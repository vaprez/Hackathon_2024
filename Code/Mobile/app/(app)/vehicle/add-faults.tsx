import StyledButton from "@/components/StyledButton";
import Theme from "@/constants/Theme";
import { AntDesign } from "@expo/vector-icons";
import axios from "axios";
import { router, useLocalSearchParams } from "expo-router";
import { useEffect, useState } from "react";
import {
  Alert,
  FlatList,
  Platform,
  StyleSheet,
  Text,
  TextInput,
  View,
} from "react-native";
import { Dropdown } from "react-native-element-dropdown";

interface TypeDefaut {
  categorie: string;
  id_defaut: number;
}

interface TypeDefautSaved {
  id_defaut: number;
  categorie: string;
  commentaire: string;
}

type ScreenParams = {
  registration: string;
};

export default function AddFaultsScreen() {
  const { registration } = useLocalSearchParams<ScreenParams>();

  const [faults, setFaults] = useState<TypeDefaut[]>([]);
  const [selectedFault, setSelectedFault] = useState<TypeDefaut | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [savedFaults, setSavedFaults] = useState<TypeDefautSaved[]>([]);
  const [comment, setComment] = useState("");
  const [isFocus, setIsFocus] = useState(false);

  useEffect(() => {
    const fetchFaults = async () => {
      try {
        const response = await axios.get<TypeDefaut[]>(
          "http://gelk.fr:5000/typedefauts"
        );
        setFaults(response.data);
        setSelectedFault(response.data[0]);
        setIsLoading(false);
      } catch (error: any) {
        console.error("Error fetching faults", error);
        Alert.alert("Error fetching faults", error.message);
      }
    };
    fetchFaults();
  }, []);

  const handleAddFaults = () => {
    // Vérifiez explicitement que selectedFault est défini
    if (selectedFault !== undefined) {
      const selectedType = faults.find((item) => {
        return Number(item.id_defaut) === Number(selectedFault?.id_defaut);
      });

      if (selectedType) {
        setSavedFaults((p) => [
          ...p,
          {
            id_defaut: selectedType.id_defaut,
            categorie: selectedType.categorie,
            commentaire: comment,
          },
        ]);
        setComment("");
      }
    } else {
      // Gérez le cas où aucun défaut n'est sélectionné
      Alert.alert("Erreur", "Veuillez sélectionner un défaut");
    }
  };

  const handleSaveFaults = async () => {
    try {
      const payload = savedFaults.map((item) => ({
        immat: registration,
        id_defaut: item.id_defaut,
        commentaire_libre: item.commentaire,
      }));
      console.log("payload", payload);
      const res = await axios.post(
        "http://gelk.fr:5000/voiture/add_defauts",
        payload
      );
      if (res.status == 201) {
        Alert.alert("Défauts enregistrés avec succès");
        router.back();
      }
    } catch (error: any) {
      console.error("Error saving faults", error);
      Alert.alert("Error saving faults", error.message);
    }
  };

  if (isLoading) {
    return <Text>Loading...</Text>;
  }

  return (
    <View style={styles.container}>
      <View style={{ gap: 20, flex: 1 }}>
        <View style={styles.inputContainer}>
          <Text>Prendre une photo</Text>
          <StyledButton label="Prendre une photo" onPress={() => {}} />
        </View>
        <View style={styles.inputContainer}>
          <Text>Catégorie</Text>
          <Dropdown
            style={[
              styles.dropdown,
              isFocus && { borderColor: Theme.backgroud },
            ]}
            placeholderStyle={styles.placeholderStyle}
            selectedTextStyle={styles.selectedTextStyle}
            inputSearchStyle={styles.inputSearchStyle}
            iconStyle={styles.iconStyle}
            data={faults}
            search
            maxHeight={300}
            labelField="categorie"
            valueField="id_defaut"
            placeholder={!isFocus ? "Select item" : "..."}
            searchPlaceholder="Rechercher..."
            value={selectedFault}
            onFocus={() => setIsFocus(true)}
            onBlur={() => setIsFocus(false)}
            onChange={(item) => {
              setSelectedFault(item);
              setIsFocus(false);
            }}
          />
        </View>
        <View style={styles.inputContainer}>
          <Text>Commentaire</Text>
          <TextInput
            style={styles.input}
            multiline
            numberOfLines={3}
            value={comment}
            onChangeText={setComment}
          />
        </View>
        <StyledButton
          label="Ajouter"
          onPress={handleAddFaults}
          variant="secondary"
        />
      </View>

      <View style={{ gap: 10 }}>
        <Text>Les défauts ajoutés apparaîtront ici</Text>
        <View style={styles.box}>
          <FlatList
            data={savedFaults}
            renderItem={({ item }) => (
              <Text>{`\u2022 ${item.categorie} ${
                item.commentaire && "- " + item.commentaire
              }`}</Text>
            )}
            keyExtractor={(_, idx) => idx.toString()}
          />
        </View>
        <StyledButton
          label="Enregistrer"
          onPress={handleSaveFaults}
          disabled={savedFaults.length === 0}
        />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    gap: 20,
    paddingBottom: 30,
  },
  box: {
    maxHeight: 100,
    overflow: "scroll",
    borderWidth: 1,
    borderColor: "#d9d9d9",
    padding: 10,
    borderRadius: 8,
  },
  inputContainer: {
    gap: 10,
  },
  input: {
    height: 70,
    paddingVertical: 8,
    paddingHorizontal: 10,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: "#d9d9d9",
  },

  dropdown: {
    height: 50,
    borderColor: "gray",
    borderWidth: 0.5,
    borderRadius: 8,
    paddingHorizontal: 8,
  },
  icon: {
    marginRight: 5,
  },
  label: {
    position: "absolute",
    backgroundColor: "white",
    left: 22,
    top: 8,
    zIndex: 999,
    paddingHorizontal: 8,
    fontSize: 14,
  },
  placeholderStyle: {
    fontSize: 16,
  },
  selectedTextStyle: {
    fontSize: 16,
  },
  iconStyle: {
    width: 20,
    height: 20,
  },
  inputSearchStyle: {
    height: 40,
    fontSize: 16,
  },
});

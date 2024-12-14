import Center from "@/components/Center";
import StyledButton from "@/components/StyledButton";
import { API_URL } from "@/constants/Api";
import Theme from "@/constants/Theme";
import { useFileUpload } from "@/hooks/useFileUpload";
import axios from "axios";
import * as FileSystem from "expo-file-system";
import { router, useLocalSearchParams } from "expo-router";
import { useEffect, useState } from "react";
import {
  Alert,
  FlatList,
  Keyboard,
  StyleSheet,
  Text,
  TextInput,
  TouchableWithoutFeedback,
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
  const [photo, setPhotos] = useState<string | null>(null);

  useEffect(() => {
    const fetchFaults = async () => {
      try {
        const response = await axios.get<TypeDefaut[]>(
          `${API_URL}/typedefauts`
        );
        setFaults(response.data);
        setSelectedFault(response.data[0]);
        setIsLoading(false);
      } catch (error: any) {
        // console.error("Error fetching faults", error);
        Alert.alert("Error fetching faults", error.message);
      }
    };
    fetchFaults();
  }, []);

  const { handleTakePicture } = useFileUpload(async (formData) => {
    try {
      setIsLoading(true);
      const file = formData.get("file") as {
        uri: string;
        type: string;
        name: string;
      } | null;
      if (!file) return;

      const base64 = await FileSystem.readAsStringAsync(file.uri, {
        encoding: "base64",
      });

      const response = await axios.post(
        `${API_URL}/vehicule/add_photo_defaut`,
        {
          blob: base64,
          extension: file.type,
        }
      );
      if (response.status == 200 && response.data) {
        setIsLoading(false);
        setPhotos(response.data.url);
      }
    } catch (error) {
      setIsLoading(false);
      // console.error(error);
      Alert.alert(
        "Erreur",
        "Une erreur est survenue lors de la prise de photo"
      );
    }
  });

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
      const res = await axios.post(`${API_URL}/voiture/add_defauts`, payload);
      if (res.status == 201) {
        Alert.alert("Défauts enregistrés avec succès");
        router.back();
      }
    } catch (error: any) {
      // console.error("Error saving faults", error);
      Alert.alert("Error saving faults", error.message);
    }
  };

  if (isLoading) {
    return (
      <Center>
        <Text>Chargement...</Text>
      </Center>
    );
  }

  return (
    <TouchableWithoutFeedback onPress={Keyboard.dismiss} accessible={false}>
      <View style={styles.container}>
        <View style={{ gap: 20, flex: 1 }}>
          <View style={styles.inputContainer}>
            <Text>Prendre une photo</Text>
            {photo ? (
              <Text style={styles.saveText}>Image enregistré.</Text>
            ) : (
              <StyledButton
                label="Prendre une photo"
                onPress={handleTakePicture}
              />
            )}
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
    </TouchableWithoutFeedback>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    gap: 20,
    paddingBottom: 30,
  },
  saveText: {
    fontSize: 18,
    color: Theme.primary,
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

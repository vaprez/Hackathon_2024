import Center from "@/components/Center";
import StyledButton from "@/components/StyledButton";
import { useFileUpload } from "@/hooks/useFileUpload";
import { Ionicons } from "@expo/vector-icons";
import axios from "axios";
import { router, Stack, useLocalSearchParams } from "expo-router";
import { useEffect, useState } from "react";
import {
  Alert,
  FlatList,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from "react-native";

type ScreenParams = {
  registration: string;
};

type DefautsRemarque = {
  id_remarque: number;
  immat: string;
  date_remarque: string;
  id_categorie: number;
  commentaire_libre: string;
  categorie: string;
};

export default function DetailsScreen() {
  const { registration } = useLocalSearchParams<ScreenParams>();

  const [isLoading, setIsLoading] = useState(true);
  const [defauts, setDefauts] = useState<DefautsRemarque[]>([]);

  useEffect(() => {
    const fetchDefauts = async () => {
      if (!registration) return;
      try {
        const response = await axios.get<DefautsRemarque[]>(
          `http://gelk.fr:5000/voiture/${registration}/defauts`
        );
        setDefauts(response.data);
        setIsLoading(false);
      } catch (error: any) {
        console.error("Error fetching faults", error);
        Alert.alert("Error fetching faults", error.message);
      }
    };
    fetchDefauts();
  }, [registration]);

  const { handleTakePicture } = useFileUpload(async (formData) => {
    console.log("Uploading file", formData.get("file"));
  });

  const handleDeleteDefaut = (id_remarque: number) => {
    Alert.alert(
      "Supprimer le défaut",
      "Êtes-vous sûr de vouloir supprimer ce défaut ?",
      [
        {
          text: "Annuler",
          style: "cancel",
        },
        {
          text: "Supprimer",
          style: "destructive",
          onPress: () => {
            setDefauts((p) =>
              p.filter((item) => item.id_remarque !== id_remarque)
            );
          },
        },
      ]
    );
  };

  if (isLoading) {
    return (
      <Center>
        <Text>Chargement...</Text>
      </Center>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.section}>
        <View style={styles.header}>
          <Text style={styles.headerTitle}>Relevé km.</Text>
          <Text>
            Dernier relevé: <Text style={{ fontWeight: "bold" }}>13792 km</Text>
          </Text>
        </View>
        <View style={styles.main}>
          <View style={styles.inputContainer}>
            <TextInput style={styles.input} placeholder="13210" />
            <StyledButton label="Enregistrer" onPress={() => {}} />
          </View>
          <StyledButton label="Prendre une photo" onPress={handleTakePicture} />
        </View>
      </View>

      <View style={[{ flex: 1, paddingBottom: 50 }, styles.section]}>
        <View style={styles.header}>
          <Text style={styles.headerTitle}>
            Défauts du véhicule
            {defauts.length > 0 && ` (${defauts.length})`}
          </Text>
          <TouchableOpacity
            onPress={() =>
              router.navigate({
                pathname: "/(app)/vehicle/add-faults",
                params: { registration },
              })
            }
          >
            <Ionicons size={26} name="add-circle-outline" />
          </TouchableOpacity>
        </View>
        <View style={styles.main}>
          <FlatList
            data={defauts}
            renderItem={({ item }) => (
              <TouchableOpacity
                onPress={() => handleDeleteDefaut(item.id_remarque)}
              >
                <View style={styles.card}>
                  <View style={styles.cardHeader}>
                    <Text style={styles.cardTitle}>{item.categorie}</Text>
                    <Text style={styles.cardDate}>
                      {new Date(item.date_remarque).toLocaleDateString()}
                    </Text>
                  </View>
                  <Text style={styles.cardText}>{item.commentaire_libre}</Text>
                </View>
              </TouchableOpacity>
            )}
            keyExtractor={(_, idx) => idx.toString()}
            ListEmptyComponent={() => (
              <Center>
                <Text>Aucun défaut enregistré. 😁</Text>
              </Center>
            )}
          />
        </View>
      </View>

      <Stack.Screen
        options={{
          headerTitle: registration,
        }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    gap: 50,
  },
  section: {
    gap: 10,
  },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: "bold",
  },
  main: {
    gap: 10,
  },
  inputContainer: {
    flexDirection: "row",
    gap: 10,
    alignItems: "stretch",
  },
  input: {
    flex: 1,
    paddingHorizontal: 10,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: "#d9d9d9",
  },
  card: {
    padding: 10,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: "#d9d9d9",
    marginBottom: 10,
  },
  cardHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
  },
  cardTitle: {
    fontSize: 16,
    fontWeight: "bold",
  },
  cardText: {
    fontSize: 14,
  },
  cardDate: {
    fontSize: 12,
    color: "#666",
  },
});

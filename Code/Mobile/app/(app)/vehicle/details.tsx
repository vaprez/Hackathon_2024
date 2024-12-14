import Center from "@/components/Center";
import StyledButton from "@/components/StyledButton";
import { API_URL } from "@/constants/Api";
import { useFileUpload } from "@/hooks/useFileUpload";
import { Ionicons } from "@expo/vector-icons";
import { useFocusEffect } from "@react-navigation/native";
import axios from "axios";
import * as FileSystem from "expo-file-system";
import { router, Stack, useLocalSearchParams } from "expo-router";
import { useCallback, useEffect, useState } from "react";
import {
  Alert,
  FlatList,
  Keyboard,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  TouchableWithoutFeedback,
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

  const [refetching, setRefetching] = useState(false);
  const [dernierReleve, setDernierReleve] = useState<number | null>(null);
  const [releveKm, setReleveKm] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [defauts, setDefauts] = useState<DefautsRemarque[]>([]);

  useFocusEffect(
    useCallback(() => {
      setRefetching((p) => !p);
    }, [])
  );

  useEffect(() => {
    const fetchDefauts = async () => {
      if (!registration) return;
      try {
        const response = await axios.get<DefautsRemarque[]>(
          `${API_URL}/voiture/${registration}/defauts`
        );
        setDefauts(response.data);
        setIsLoading(false);
      } catch (error: any) {
        // console.error("Error fetching faults", error);
        Alert.alert("Error fetching faults", error.message);
      }
    };
    const fetchDernierReleve = async () => {
      if (!registration) return;
      try {
        const response = await axios.get<any>(
          `${API_URL}/voiture/${registration}/dernier_kilometrage`
        );
        if (response.status == 200 && response.data) {
          setDernierReleve(response.data.releve_km);
        }
      } catch (error: any) {
        // console.error("Error fetching km", error);
        Alert.alert("Error fetching km", error.message);
      }
    };
    fetchDefauts();
    fetchDernierReleve();
  }, [registration, refetching]);

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

      const response = await axios.post(`${API_URL}/vehicule/compteur`, {
        blob: base64,
        extension: file.type,
      });
      if (response.status == 200 && response.data) {
        setIsLoading(false);
        setReleveKm(response.data.toString());
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

  const handleAddKilemetrage = () => {
    if (!releveKm) return;
    Alert.alert(
      "Enregistrer le relevé kilométrique",
      `Êtes-vous sûr de vouloir enregistrer le relevé kilométrique à ${releveKm} km ?`,
      [
        {
          text: "Annuler",
          style: "cancel",
        },
        {
          text: "Enregistrer",
          style: "default",
          onPress: async () => {
            try {
              setIsLoading(true);
              const response = await axios.post(
                `${API_URL}/voiture/${registration}/kilometrage`,
                {
                  source_releve: "appli",
                  releve_km: parseInt(releveKm),
                }
              );
              if (response.status == 201) {
                setIsLoading(false);
                Alert.alert(
                  "Relevé km enregistré",
                  "Le relevé km a été enregistré avec succès."
                );
                setRefetching((p) => !p);
              }
            } catch (error: any) {
              setIsLoading(false);
              // console.error("Error saving km", error);
              Alert.alert("Error saving km", error.message);
            }
          },
        },
      ]
    );
  };

  return (
    <TouchableWithoutFeedback onPress={Keyboard.dismiss} accessible={false}>
      <View style={styles.container}>
        <View style={styles.section}>
          <View style={styles.header}>
            <Text style={styles.headerTitle}>Relevé km.</Text>
            <Text>
              Dernier relevé:{" "}
              <Text style={{ fontWeight: "bold" }}>{dernierReleve} km</Text>
            </Text>
          </View>
          <View style={styles.main}>
            <View style={styles.inputContainer}>
              <TextInput
                value={releveKm}
                style={styles.input}
                onChangeText={setReleveKm}
              />
              <StyledButton
                label="Enregistrer"
                onPress={handleAddKilemetrage}
              />
            </View>
            <StyledButton
              label="Prendre une photo"
              onPress={handleTakePicture}
              isLoading={isLoading}
            />
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
                    <Text style={styles.cardText}>
                      {item.commentaire_libre}
                    </Text>
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
    </TouchableWithoutFeedback>
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

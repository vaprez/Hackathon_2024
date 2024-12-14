import StyledButton from "@/components/StyledButton";
import { API_URL } from "@/constants/Api";
import { useFileUpload } from "@/hooks/useFileUpload";
import { Ionicons } from "@expo/vector-icons";
import axios from "axios";
import * as FileSystem from "expo-file-system";
import { router } from "expo-router";
import { StatusBar } from "expo-status-bar";
import { useState } from "react";
import {
  Alert,
  Keyboard,
  StyleSheet,
  Text,
  TextInput,
  TouchableWithoutFeedback,
  View,
} from "react-native";

export default function TabOneScreen() {
  const [registration, setRegistration] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);

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

      const response = await axios.post(`${API_URL}/vehicule/immat_ocr`, {
        blob: base64,
        extension: file.type,
      });
      if (response.status == 200 && response.data) {
        setIsLoading(false);
        setRegistration(response.data);
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

  const handleSearch = () => {
    if (!registration) return;
    router.navigate({
      pathname: "/(app)/vehicle/details",
      params: {
        registration,
      },
    });
  };

  return (
    <TouchableWithoutFeedback onPress={Keyboard.dismiss} accessible={false}>
      <View style={styles.container}>
        <View>
          <View style={styles.searchContainer}>
            <Text>Recherche par plaque d'immatriculation</Text>
            <View style={styles.inputContainer}>
              <TextInput
                style={styles.input}
                value={registration}
                placeholder="AB-123-CD"
                onChangeText={setRegistration}
              />
              <StyledButton
                label="Rechercher"
                onPress={handleSearch}
                disabled={!registration}
              />
            </View>
          </View>
          <View style={styles.separator} />
          <StyledButton
            label="Prise de photo"
            onPress={handleTakePicture}
            isLoading={isLoading}
          />
        </View>

        <View style={{ gap: 20 }}>
          <View style={{ flexDirection: "row", gap: 10 }}>
            <Ionicons
              name="information-circle"
              size={24}
              color="black"
              style={{ marginBottom: 10 }}
            />
            <Text style={styles.title}>
              Conseil pour prendre une bonne photo
            </Text>
          </View>
          <View>
            <Text style={{ fontSize: 16 }}>
              - Cadrer le sujet au centre de l'image
            </Text>
            <Text style={{ fontSize: 16 }}>
              - Assurez-vous que la plaque soit lisible
            </Text>
            <Text style={{ fontSize: 16 }}>
              - Evitez les reflets et les ombres
            </Text>
            <Text style={{ fontSize: 16 }}>- Prenez la photo de près</Text>
            <Text style={{ fontSize: 16 }}>- Rester stable</Text>
          </View>
        </View>

        <StatusBar style="light" />
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
  title: {
    fontSize: 20,
    fontWeight: "bold",
  },
  separator: {
    alignSelf: "center",
    marginVertical: 30,
    height: 1,
    width: "80%",
    backgroundColor: "#d9d9d9",
  },
  searchContainer: {
    flexDirection: "column",
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
});

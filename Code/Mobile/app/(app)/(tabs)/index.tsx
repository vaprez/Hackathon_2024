import StyledButton from "@/components/StyledButton";
import { useFileUpload } from "@/hooks/useFileUpload";
import axios from "axios";
import * as FileSystem from "expo-file-system";
import { router } from "expo-router";
import { StatusBar } from "expo-status-bar";
import { useState } from "react";
import { Alert, StyleSheet, Text, TextInput, View } from "react-native";

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

      const response = await axios.post(
        "http://gelk.fr:5000/vehicule/immat_ocr",
        {
          blob: base64,
          extension: file.type,
        }
      );
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
    router.navigate({
      pathname: "/(app)/vehicle/details",
      params: {
        registration,
      },
    });
  };

  return (
    <View style={styles.container}>
      <View style={styles.searchContainer}>
        <Text>Recherche par plaque d'immatriculation</Text>
        <View style={styles.inputContainer}>
          <TextInput
            style={styles.input}
            value={registration}
            placeholder="AB-123-CD"
          />
          <StyledButton label="Rechercher" onPress={handleSearch} />
        </View>
      </View>
      <View style={styles.separator} />
      <StyledButton
        label="Prise de photo"
        onPress={handleTakePicture}
        isLoading={isLoading}
      />

      <StatusBar style="light" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
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

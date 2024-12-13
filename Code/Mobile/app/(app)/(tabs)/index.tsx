import StyledButton from "@/components/StyledButton";
import { useFileUpload } from "@/hooks/useFileUpload";
import { router } from "expo-router";
import { StatusBar } from "expo-status-bar";
import { useState } from "react";
import { StyleSheet, Text, TextInput, View } from "react-native";

export default function TabOneScreen() {
  const [registration, setRegistration] = useState<string>("AB123CD");

  const { handleTakePicture } = useFileUpload(async (formData) => {
    console.log("Uploading file", formData.get("file"));
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
      <StyledButton label="Prise de photo" onPress={handleTakePicture} />

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

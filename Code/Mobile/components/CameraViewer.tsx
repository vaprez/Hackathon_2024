import { CameraView, useCameraPermissions } from "expo-camera";
import { useState } from "react";
import { StyleSheet, Text, TouchableOpacity, View } from "react-native";
import StyledButton from "./StyledButton";

export default function CameraViewer() {
  const [torch, setTorch] = useState(false);
  const [permission, requestPermission] = useCameraPermissions();

  const toggleTorch = () => {
    setTorch(!torch);
  };

  if (!permission) {
    // Camera permissions are still loading.
    return <View />;
  }

  if (!permission.granted) {
    // Camera permissions are not granted yet.
    return (
      <View style={styles.container}>
        <Text style={styles.message}>
          Nous avons besoin de votre permission pour accéder à la caméra.
        </Text>
        <StyledButton onPress={requestPermission} label="Autoriser la caméra" />
      </View>
    );
  }

  return (
    <CameraView style={styles.camera} enableTorch={torch}>
      <View style={styles.buttonContainer}>
        <TouchableOpacity style={styles.button} onPress={toggleTorch}>
          <Text style={styles.text}>Activer le flash</Text>
        </TouchableOpacity>
      </View>
    </CameraView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 30,
    justifyContent: "center",
    gap: 50,
    paddingBottom: 100,
  },
  message: {
    textAlign: "center",
    paddingBottom: 10,
  },
  camera: {
    flex: 1,
    borderRadius: 20,
  },
  buttonContainer: {
    flex: 1,
    flexDirection: "row",
    backgroundColor: "transparent",
    margin: 24,
  },
  button: {
    flex: 1,
    alignSelf: "flex-end",
    alignItems: "center",
  },
  text: {
    fontSize: 18,
    fontWeight: "bold",
    color: "white",
  },
});

import StyledButton from "@/components/StyledButton";
import { router } from "expo-router";
import { StyleSheet, View } from "react-native";

export default function ScanRegistrationScreen() {
  return (
    <View style={styles.container}>
      <StyledButton
        label="Valider"
        onPress={() =>
          router.navigate({
            pathname: "/(app)/vehicle/details",
            params: {
              registration: "AA-123-BB",
            },
          })
        }
      />
    </View>
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

import { Button, StyleSheet, TextInput } from "react-native";

import StyledButton from "@/components/StyledButton";
import Theme from "@/constants/Theme";
import { Image } from "expo-image";
import { router } from "expo-router";
import { Text, View } from "react-native";

export default function LoginScreen() {
  const username = "user1";
  const password = "password1";

  return (
    <View style={styles.container}>
      <Image
        style={styles.logo}
        source={require("../assets/images/logo-edf.svg")}
        contentFit="contain"
        transition={200}
      />
      <View style={styles.main}>
        <Text style={styles.title}>
          Connexion à l'espace de gestion de véhicule
        </Text>
        <View style={styles.form}>
          <TextInput
            style={styles.input}
            value={username}
            placeholder="Nom d'utilisateur"
          />
          <TextInput
            style={styles.input}
            value={password}
            secureTextEntry={true}
            placeholder="Mot de passe"
          />
          <Text
            style={{
              fontSize: 12,
              color: Theme.primary,
              textDecorationLine: "underline",
            }}
          >
            Mot de passe oublié ?
          </Text>
          <StyledButton
            label="Se connecter"
            onPress={() => router.replace("/(app)/(tabs)")}
          />
        </View>
      </View>
      <Image
        style={styles.asset}
        source={require("../assets/images/asset.svg")}
        contentFit="cover"
        transition={200}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 40,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: Theme.backgroud,
  },
  main: {
    flex: 3,
    gap: 20,
  },
  form: {
    backgroundColor: "white",
    padding: 20,
    gap: 20,
    zIndex: 1,
  },
  input: {
    height: 44,
    paddingHorizontal: 10,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: "#d9d9d9",
  },
  logo: {
    flex: 1,
    width: "100%",
  },
  title: {
    fontSize: 36,
    color: Theme.text,
  },
  asset: {
    flex: 1,
    width: 400,
    height: 300,
    position: "absolute",
    left: 0,
    bottom: 0,
  },
});

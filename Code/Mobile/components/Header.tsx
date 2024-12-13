import Theme from "@/constants/Theme";
import { Feather, Ionicons } from "@expo/vector-icons";
import { NativeStackHeaderProps } from "@react-navigation/native-stack/lib/typescript/module/src/types";
import { useRouter } from "expo-router";
import { Pressable, StyleSheet, Text, View } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";

export default function Header(props: NativeStackHeaderProps) {
  const insets = useSafeAreaInsets();

  return (
    <View
      style={{
        paddingTop: insets.top + 10,
        ...styles.header,
      }}
    >
      <Pressable
        style={styles.headerBack}
        onPress={props.navigation.goBack}
        hitSlop={10}
      >
        <Feather name="chevron-left" size={26} color="white" />
      </Pressable>
      <Text style={styles.headerText}>
        {(props.options?.headerTitle as string) ?? "Header"}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  header: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 40,
    color: "white",
    backgroundColor: Theme.backgroud,
    paddingHorizontal: 20,
    paddingBottom: 20,
  },
  headerBack: {
    position: "absolute",
    left: 20,
    bottom: 16,
  },
  headerText: {
    color: "white",
    fontSize: 18,
    fontWeight: "bold",
  },
});

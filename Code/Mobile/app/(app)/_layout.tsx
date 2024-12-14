import Header from "@/components/Header";
import { Stack } from "expo-router";

export default function AppLayout() {
  return (
    <Stack
      screenOptions={{
        header: (props) => <Header {...props} />,
      }}
    >
      <Stack.Screen
        name="(tabs)"
        options={{ headerShown: false, headerTitle: "Home" }}
      />

      <Stack.Screen
        name="vehicle/details"
        options={{
          headerTitle: "Voiture",
        }}
      />
      <Stack.Screen
        name="vehicle/scan-registration"
        options={{
          headerTitle: "Prise de photo",
        }}
      />
      <Stack.Screen
        name="vehicle/add-faults"
        options={{
          headerTitle: "Ajouter des défauts",
        }}
      />
    </Stack>
  );
}

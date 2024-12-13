import { MaterialCommunityIcons } from "@expo/vector-icons";
import { Link, Tabs } from "expo-router";
import React from "react";

// You can explore the built-in icon families and icons on the web at https://icons.expo.fyi/
function TabBarIcon(props: {
  name: React.ComponentProps<typeof MaterialCommunityIcons>["name"];
  color: string;
}) {
  return <MaterialCommunityIcons size={28} {...props} />;
}

export default function TabLayout() {
  return (
    <Tabs
      screenOptions={{
        headerStyle: {
          backgroundColor: "#001A70",
        },
        headerTitleStyle: {
          color: "white",
        },
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: "EDF - Gestion des véhicules",
          tabBarLabel: "Véhicules",
          tabBarIcon: ({ color }) => (
            <TabBarIcon name="van-utility" color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="inspection"
        options={{
          title: "EDF - Inspection des véhicules",
          tabBarLabel: "Inspection",
          tabBarIcon: ({ color }) => (
            <TabBarIcon name="car-info" color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="reservation"
        options={{
          title: "EDF - Réservation & Covoiturage",
          tabBarLabel: "Réserver",
          tabBarIcon: ({ color }) => (
            <TabBarIcon name="car-clock" color={color} />
          ),
        }}
      />
    </Tabs>
  );
}

import Center from "@/components/Center";
import StyledButton from "@/components/StyledButton";
import { API_URL } from "@/constants/Api";
import Theme from "@/constants/Theme";
import { Ionicons } from "@expo/vector-icons";
import axios from "axios";
import { useEffect, useState } from "react";
import {
  Alert,
  FlatList,
  Keyboard,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  TouchableWithoutFeedback,
  View,
} from "react-native";
import CalendarPicker from "react-native-calendar-picker";
import { Dropdown } from "react-native-element-dropdown";

type Destination = {
  id_destination: number;
  lat: number;
  lon: number;
  nom_destination: string;
};

export default function TabTwoScreen() {
  const [isLoading, setIsLoading] = useState(false);
  const [destDepartFocus, setDestDepartFocus] = useState(false);
  const [destArriveeFocus, setDestArriveeFocus] = useState(false);
  const [destDepart, setDestDepart] = useState<Destination | null>(null);
  const [destArrivee, setDestArrivee] = useState<Destination | null>(null);
  const [selectedStartDate, setSelectedStartDate] = useState<Date | null>(null);
  const [selectedEndDate, setSelectedEndDate] = useState<Date | null>(null);
  const [selectedNbPersonnes, setSelectedNbPersonnes] = useState("1");
  const [destinations, setDestinations] = useState<Destination[]>([]);

  useEffect(() => {
    const fetchDestinations = async () => {
      try {
        const response = await axios.get<Destination[]>(
          `${API_URL}/destinations`
        );
        if (response.data.length === 0) {
          Alert.alert("Aucune destination trouvée");
          return;
        }
        setDestinations(response.data);
      } catch (error: any) {
        Alert.alert(
          "Erreur dans la récupération des destinations",
          error.message
        );
      }
    };
    fetchDestinations();
  }, []);

  const onDateChange = (date: Date, type: string) => {
    if (type === "END_DATE") {
      setSelectedEndDate(date);
    } else {
      setSelectedStartDate(date);
      setSelectedEndDate(null);
    }
  };

  const handleSearch = async () => {
    try {
      if (
        !destDepart ||
        !destArrivee ||
        !selectedStartDate ||
        !selectedEndDate
      ) {
        Alert.alert("Veuillez remplir tous les champs");
        return;
      }

      const response = await axios.post<{
        reservations_covoiturage: any[];
        vehicules_disponibles: any[];
      }>(`${API_URL}/search_reservations`, {
        depart: destDepart.id_destination,
        arrivee: destArrivee.id_destination,
        date_debut: selectedStartDate,
        date_fin: selectedEndDate,
        nb_personnes: selectedNbPersonnes,
      });
      console.log(response.data.reservations_covoiturage);
      // if (response.data) {
      //   Alert.alert("Aucun véhicule trouvé");
      //   return;
      // }
      setIsLoading(false);
    } catch (error: any) {
      Alert.alert("Erreur dans la recherche", error.message);
    }
  };

  if (isLoading) {
    return (
      <Center>
        <Text>Chargement ...</Text>
      </Center>
    );
  }

  return (
    <TouchableWithoutFeedback onPress={Keyboard.dismiss} accessible={false}>
      <View style={styles.container}>
        <Text style={styles.title}>Reservation d'un véhicule</Text>
        <View style={styles.inputContainer}>
          <View>
            <Dropdown
              style={[
                styles.dropdown,
                destDepartFocus && { borderColor: Theme.backgroud },
              ]}
              placeholderStyle={styles.placeholderStyle}
              selectedTextStyle={styles.selectedTextStyle}
              inputSearchStyle={styles.inputSearchStyle}
              iconStyle={styles.iconStyle}
              data={destinations}
              search
              maxHeight={300}
              labelField="nom_destination"
              valueField="id_destination"
              placeholder={!destDepartFocus ? "Destination de départ" : "..."}
              searchPlaceholder="Rechercher..."
              value={destDepart}
              onFocus={() => setDestDepartFocus(true)}
              onBlur={() => setDestDepartFocus(false)}
              onChange={(item) => {
                setDestDepart(item);
                setDestDepartFocus(false);
              }}
            />
          </View>
          <View>
            <Dropdown
              style={[
                styles.dropdown,
                destArriveeFocus && { borderColor: Theme.backgroud },
              ]}
              placeholderStyle={styles.placeholderStyle}
              selectedTextStyle={styles.selectedTextStyle}
              inputSearchStyle={styles.inputSearchStyle}
              iconStyle={styles.iconStyle}
              data={destinations}
              search
              maxHeight={300}
              labelField="nom_destination"
              valueField="id_destination"
              placeholder={!destDepartFocus ? "Destination d'arrivée" : "..."}
              searchPlaceholder="Rechercher..."
              value={destArrivee}
              onFocus={() => setDestArriveeFocus(true)}
              onBlur={() => setDestArriveeFocus(false)}
              onChange={(item) => {
                setDestArrivee(item);
                setDestArriveeFocus(false);
              }}
            />
          </View>
          <View>
            <Ionicons
              name="people-outline"
              size={20}
              color="black"
              style={styles.icon}
            />
            <TextInput
              style={styles.input}
              placeholder="Nombre de passager"
              value={selectedNbPersonnes}
              onChangeText={setSelectedNbPersonnes}
            />
          </View>
        </View>
        <CalendarPicker
          startFromMonday={true}
          allowRangeSelection={true}
          todayBackgroundColor={Theme.primary}
          selectedDayColor={Theme.primary}
          selectedDayTextColor="#FFFFFF"
          onDateChange={onDateChange}
        />
        <StyledButton label="Réserver" onPress={handleSearch} />
      </View>
    </TouchableWithoutFeedback>
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
    marginBottom: 10,
  },
  flexContainer: {
    flexDirection: "row",
    gap: 10,
  },
  icon: {
    position: "absolute",
    top: 12,
    left: 12,
  },
  inputContainer: {
    gap: 10,
    marginBottom: 20,
  },
  input: {
    height: 44,
    paddingVertical: 8,
    paddingLeft: 40,
    paddingHorizontal: 10,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: "#d9d9d9",
  },
  inputFlex: {
    flex: 1,
    position: "relative",
  },

  //Dropdown

  dropdown: {
    height: 50,
    borderColor: "#d9d9d9",
    borderWidth: 0.5,
    borderRadius: 8,
    paddingHorizontal: 8,
  },
  // icon: {
  //   marginRight: 5,
  // },
  label: {
    position: "absolute",
    backgroundColor: "white",
    left: 22,
    top: 8,
    zIndex: 999,
    paddingHorizontal: 8,
    fontSize: 12,
  },
  placeholderStyle: {
    fontSize: 14,
    color: "#aaa",
  },
  selectedTextStyle: {
    fontSize: 16,
  },
  iconStyle: {
    width: 20,
    height: 20,
  },
  inputSearchStyle: {
    height: 40,
    fontSize: 16,
  },
});

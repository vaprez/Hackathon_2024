import { createFileObject, getFormattedDateString } from "@/utils";
import * as DocumentPicker from "expo-document-picker";
import * as ImagePicker from "expo-image-picker";
import { Alert } from "react-native";

export function useFileUpload(
  uploadCallback: (formData: FormData) => Promise<any>
) {
  const handleImagePicker = async () => {
    try {
      const image = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ["images"],
        quality: 0.5,
      });
      if (image.canceled) return;

      const defaultFileName = getFormattedDateString() + ".jpg";
      const file = await createFileObject({
        name: image.assets[0].fileName || defaultFileName,
        type: image.assets[0].mimeType || "image/jpeg",
        uri: image.assets[0].uri,
      });

      const formData = new FormData();
      formData.append("file", file as any, file.name);

      const res = await uploadCallback(formData);
      if (res) {
        Alert.alert("Succès", "L'image a bien été envoyée");
      }
    } catch (error: any) {
      Alert.alert("Erreur", error.message);
    }
  };

  const handleTakePicture = async () => {
    try {
      const image = await ImagePicker.launchCameraAsync({
        mediaTypes: "images",
        quality: 0.5,
      });

      if (image.canceled) return;

      const defaultFileName = getFormattedDateString() + ".jpg";
      const file = await createFileObject({
        name: image.assets[0].fileName || defaultFileName,
        type: image.assets[0].mimeType || "image/jpeg",
        uri: image.assets[0].uri,
      });

      const formData = new FormData();
      formData.append("file", file as any, file.name);

      const res = await uploadCallback(formData);
      if (res) {
        Alert.alert("Succès", "L'image a bien été envoyée");
      }
    } catch (error: any) {
      Alert.alert("Erreur", error.message);
    }
  };

  return {
    handleImagePicker,
    handleTakePicture,
  };
}

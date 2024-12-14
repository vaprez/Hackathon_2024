import axios from "axios";
import * as FileSystem from "expo-file-system";
import { Platform } from "react-native";

export type FileObject = {
  name: string;
  type: string;
  uri: string;
};

export const getFormattedDateString = (date: Date = new Date()): string => {
  const now = date;
  const year = now.getFullYear().toString().slice(-2); // Get last two digits of the year
  const month = String(now.getMonth() + 1).padStart(2, "0"); // Month starts from 0
  const day = String(now.getDate()).padStart(2, "0");
  const hours = String(now.getHours()).padStart(2, "0");
  const minutes = String(now.getMinutes()).padStart(2, "0");
  const seconds = String(now.getSeconds()).padStart(2, "0");
  return `${hours}-${minutes}-${seconds}_${day}-${month}-${year}`;
};

export const authAPI = async () => {
  return axios.create({
    baseURL: "http://gelk.fr:3000",
    headers: {},
  });
};

export const createFileObject = async (
  file: FileObject
): Promise<FileObject> => {
  // Check if fileUri is a local file or a remote one
  if (Platform.OS === "android") {
    // On Android, the file URI might be in a cache directory,
    // so we need to copy it to a more accessible location first
    const fileInfo = await FileSystem.getInfoAsync(file.uri);
    if (!fileInfo.exists) {
      throw new Error("File not found");
    }
    const newUri = `${FileSystem.documentDirectory}${file.name}`;
    await FileSystem.copyAsync({ from: file.uri, to: newUri });
    file.uri = newUri;
  }

  return {
    uri: file.uri,
    name: file.name,
    type: file.type,
  };
};

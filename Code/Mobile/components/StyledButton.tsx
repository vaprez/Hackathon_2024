import { useState } from "react";
import {
  ActivityIndicator,
  Pressable,
  PressableProps,
  StyleSheet,
  Text,
} from "react-native";

interface ButtonProps extends PressableProps {
  isLoading?: boolean;
  label?: string;
  size?: "sm" | "md" | "lg" | "xl";
  variant?: "primary" | "secondary" | "danger" | "success";
  outline?: boolean;
}

const StyledButton = ({
  isLoading,
  label,
  size = "md",
  variant = "primary",
  outline = false,
  ...props
}: ButtonProps) => {
  const [pressed, setPressed] = useState(false);

  const handlePressIn = () => {
    setPressed(true);
  };

  const handlePressOut = () => {
    setPressed(false);
  };

  return (
    <Pressable
      onPressIn={handlePressIn}
      onPressOut={handlePressOut}
      style={[
        styles.button,
        props.disabled && { opacity: 0.5 },
        variant === "primary" && {
          backgroundColor: pressed ? "#004cb3" : "#005BFF",
        },
        variant === "secondary" && {
          backgroundColor: pressed ? "#1E1E1E" : "#2C2C2C",
        },
      ]}
      {...props}
    >
      {isLoading ? (
        <ActivityIndicator size={"small"} color={"white"} />
      ) : label ? (
        <Text style={styles.text}>{label}</Text>
      ) : (
        props.children
      )}
    </Pressable>
  );
};

export default StyledButton;

const styles = StyleSheet.create({
  button: {
    alignItems: "center",
    justifyContent: "center",
    paddingHorizontal: 12,
    paddingVertical: 16,
    minHeight: 40,
  },
  text: {
    color: "white",
    fontSize: 16,
  },
});

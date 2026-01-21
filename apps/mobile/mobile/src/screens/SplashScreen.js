import React, { useEffect } from "react";
import { View, Image, StyleSheet } from "react-native";
import { theme } from "../constants/theme";

export default function SplashScreen({ onDone }) {
  useEffect(() => {
    const t = setTimeout(() => onDone?.(), 5000); // 5s
    return () => clearTimeout(t);
  }, [onDone]);

  return (
    <View style={styles.container}>
      {/* Fondo con imagen opcional */}
      <Image
        source={require("../../assets/splash-bg.png")}
        style={styles.bg}
        resizeMode="cover"
      />

      {/* Overlay para oscurecer */}
      <View style={styles.overlay} />

      {/* Logo */}
      <Image
        source={require("../../assets/logo.png")}
        style={styles.logo}
        resizeMode="contain"
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0b0f0c", alignItems: "center", justifyContent: "center" },
  bg: { ...StyleSheet.absoluteFillObject, opacity: 0.65 },
  overlay: { ...StyleSheet.absoluteFillObject, backgroundColor: "rgba(0,0,0,0.35)" },
  logo: { width: 190, height: 190 },
});

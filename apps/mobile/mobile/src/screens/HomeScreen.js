import React from "react";
import { View, Text, Pressable, StyleSheet, Image } from "react-native";
import { theme } from "../constants/theme";

export default function HomeScreen({ onOpenPlatform }) {
  return (
    <View style={styles.container}>
      <Image
        source={require("../../assets/splash-bg.png")}
        style={styles.bg}
        resizeMode="cover"
      />
      <View style={styles.overlay} />

      <View style={styles.card}>
        <Image
          source={require("../../assets/logo.png")}
          style={styles.logo}
          resizeMode="contain"
        />

        <Text style={styles.title}>
          Nutry<Text style={{ color: theme.primary }}>Gym</Text>
        </Text>

        <Text style={styles.subtitle}>
          Welcome to the NutryGym mobile demo. This app is currently informational and provides access to the web platform.
        </Text>

        <Pressable
          onPress={onOpenPlatform}
          style={({ pressed }) => [styles.btn, pressed && styles.btnPressed]}
        >
          <Text style={styles.btnText}>Open Platform</Text>
        </Pressable>

        <Pressable
          onPress={() => {}}
          style={({ pressed }) => [styles.btnGhost, pressed && styles.btnGhostPressed]}
        >
          <Text style={styles.btnGhostText}>About (Demo)</Text>
        </Pressable>

        <Text style={styles.note}>
          Tip: If the platform is down, the app will show an offline fallback screen.
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0b0f0c", justifyContent: "center", padding: 18 },
  bg: { ...StyleSheet.absoluteFillObject, opacity: 0.65 },
  overlay: { ...StyleSheet.absoluteFillObject, backgroundColor: "rgba(0,0,0,0.45)" },

  card: {
    backgroundColor: "rgba(255,255,255,0.92)",
    borderRadius: 18,
    padding: 18,
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.25)",
  },
  logo: { width: 72, height: 72, alignSelf: "center", marginBottom: 10 },
  title: { fontSize: 34, fontWeight: "900", color: theme.ink, textAlign: "center" },
  subtitle: { marginTop: 10, color: theme.muted, lineHeight: 20, textAlign: "center" },

  btn: {
    marginTop: 16,
    backgroundColor: theme.primary,
    paddingVertical: 12,
    borderRadius: 12,
    alignItems: "center",
  },
  btnPressed: { backgroundColor: theme.primaryDark },
  btnText: { color: "white", fontWeight: "900" },

  btnGhost: {
    marginTop: 10,
    backgroundColor: "transparent",
    borderWidth: 1,
    borderColor: theme.border,
    paddingVertical: 12,
    borderRadius: 12,
    alignItems: "center",
  },
  btnGhostPressed: { backgroundColor: "rgba(15,23,42,0.05)" },
  btnGhostText: { color: theme.ink, fontWeight: "900" },

  note: { marginTop: 12, fontSize: 12.5, color: theme.muted, textAlign: "center" },
});

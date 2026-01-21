import React from "react";
import { View, Text, Pressable, StyleSheet } from "react-native";
import { theme } from "../constants/theme";

export default function OfflineScreen({ onRetry }) {
  return (
    <View style={styles.container}>
      <Text style={styles.kicker}>NutryGym · Mobile</Text>

      <Text style={styles.title}>
        Nutry<Text style={styles.green}>Gym</Text>
      </Text>

      <Text style={styles.subtitle}>
        We couldn’t connect to the online platform right now.
        Please check your internet connection or try again.
      </Text>

      <Pressable
        onPress={onRetry}
        style={({ pressed }) => [styles.btn, pressed && styles.btnPressed]}
      >
        <Text style={styles.btnText}>Try again</Text>
      </Pressable>

      <View style={styles.card}>
        <Text style={styles.cardTitle}>Offline fallback</Text>
        <Text style={styles.cardDesc}>
          This mobile app reuses the NutryGym web platform via WebView. If the
          platform is unavailable, this offline screen is shown.
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.bg,
    padding: 18,
    justifyContent: "center",
  },
  kicker: {
    color: theme.muted,
    fontSize: 12,
    letterSpacing: 1.5,
    textTransform: "uppercase",
    marginBottom: 10,
  },
  title: {
    fontSize: 44,
    fontWeight: "900",
    color: theme.ink,
    marginBottom: 8,
  },
  green: { color: theme.primary },
  subtitle: {
    color: theme.muted,
    fontSize: 14.5,
    lineHeight: 22,
    marginBottom: 18,
  },
  btn: {
    backgroundColor: theme.primary,
    paddingVertical: 12,
    borderRadius: 10,
    alignItems: "center",
  },
  btnPressed: {
    backgroundColor: theme.primaryDark,
  },
  btnText: {
    color: "white",
    fontWeight: "900",
  },
  card: {
    marginTop: 14,
    backgroundColor: "white",
    borderRadius: 16,
    padding: 16,
    borderWidth: 1,
    borderColor: "rgba(15, 23, 42, 0.06)",
  },
  cardTitle: {
    color: theme.ink,
    fontWeight: "900",
    marginBottom: 6,
  },
  cardDesc: {
    color: theme.muted,
    lineHeight: 20,
  },
});

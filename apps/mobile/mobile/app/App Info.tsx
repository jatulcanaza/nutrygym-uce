import { View, Text, StyleSheet } from "react-native";

export default function AppInfo() {
  return (
    <View style={styles.container}>
      <Text style={styles.h1}>App Info</Text>
      <Text style={styles.p}>
        NutryGym mobile is a demo interface that provides informational content and access to the web platform.
      </Text>

      <View style={styles.card}>
        <Text style={styles.cardTitle}>Build</Text>
        <Text style={styles.cardText}>Version: 1.0.0</Text>
        <Text style={styles.cardText}>Expo SDK: 54</Text>
        <Text style={styles.cardText}>Platform: Android (demo)</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0b0b0c", padding: 18 },
  h1: { fontSize: 30, fontWeight: "900", color: "white", marginTop: 6 },
  p: { marginTop: 10, color: "rgba(255,255,255,0.75)", fontWeight: "700", lineHeight: 20 },
  card: { marginTop: 16, backgroundColor: "rgba(255,255,255,0.92)", borderRadius: 18, padding: 16 },
  cardTitle: { fontSize: 18, fontWeight: "900", color: "#111" },
  cardText: { marginTop: 8, color: "#333", fontWeight: "800" },
});

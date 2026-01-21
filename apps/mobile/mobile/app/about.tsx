import { View, Text, StyleSheet } from "react-native";

export default function About() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>About NutryGym</Text>
      <Text style={styles.p}>
        NutryGym is a smart nutrition and fitness platform designed for students and professionals.
        This mobile app is a demo interface and currently provides informational content and access to the web platform.
      </Text>

      <View style={styles.card}>
        <Text style={styles.cardTitle}>Key modules</Text>
        <Text style={styles.li}>• Nutrition planning (AI)</Text>
        <Text style={styles.li}>• Training guidance</Text>
        <Text style={styles.li}>• Microservices architecture (AWS)</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0b0f0c", padding: 18 },
  title: { color: "#ffffff", fontSize: 24, fontWeight: "900", marginBottom: 12 },
  p: { color: "rgba(255,255,255,0.78)", fontWeight: "700", lineHeight: 20 },

  card: { marginTop: 18, backgroundColor: "rgba(255,255,255,0.92)", borderRadius: 18, padding: 16 },
  cardTitle: { fontSize: 16, fontWeight: "900", color: "#0f172a", marginBottom: 8 },
  li: { color: "#334155", fontWeight: "700", marginTop: 6 },
});

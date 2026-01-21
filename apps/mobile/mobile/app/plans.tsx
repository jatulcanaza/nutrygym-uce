import { View, Text, StyleSheet, Pressable } from "react-native";
import { useRouter } from "expo-router";

export default function Plans() {
  const router = useRouter();

  return (
    <View style={styles.container}>
      <Text style={styles.h1}>Plans</Text>
      <Text style={styles.p}>Current demo modules available in the platform.</Text>

      <View style={styles.card}>
        <Text style={styles.badge}>AI Nutrition</Text>
        <Text style={styles.title}>NutriGym</Text>
        <Text style={styles.desc}>Personalized weekly nutrition plan generation and management.</Text>

        <Pressable style={styles.btn} onPress={() => router.push("/platform" as any)}>
          <Text style={styles.btnText}>Open Web Platform</Text>
        </Pressable>
      </View>

      <View style={styles.card}>
        <Text style={styles.badge}>Training</Text>
        <Text style={styles.title}>Gym</Text>
        <Text style={styles.desc}>Workout routines and training guidance (demo).</Text>

        <Pressable style={styles.btnOutline} onPress={() => router.push("/platform" as any)}>
          <Text style={styles.btnOutlineText}>Open Web Platform</Text>
        </Pressable>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0b0b0c", padding: 18 },
  h1: { fontSize: 30, fontWeight: "900", color: "white", marginTop: 6 },
  p: { marginTop: 6, color: "rgba(255,255,255,0.75)", fontWeight: "700" },
  card: { marginTop: 14, backgroundColor: "rgba(255,255,255,0.92)", borderRadius: 18, padding: 16 },
  badge: { alignSelf: "flex-start", backgroundColor: "#e8f5d1", paddingHorizontal: 10, paddingVertical: 6, borderRadius: 999, fontWeight: "900" },
  title: { marginTop: 10, fontSize: 24, fontWeight: "900", color: "#111" },
  desc: { marginTop: 6, color: "#333", fontWeight: "700", lineHeight: 20 },
  btn: { marginTop: 14, backgroundColor: "#80c522", paddingVertical: 14, borderRadius: 12, alignItems: "center" },
  btnText: { color: "white", fontWeight: "900" },
  btnOutline: { marginTop: 14, borderWidth: 2, borderColor: "#111", paddingVertical: 14, borderRadius: 12, alignItems: "center" },
  btnOutlineText: { color: "#111", fontWeight: "900" },
});

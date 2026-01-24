import { View, Text, Image, StyleSheet, Pressable } from "react-native";
import { useRouter } from "expo-router";

const WEB_URL = "http://nutrygym-uce-qa-alb-1894441400.us-east-1.elb.amazonaws.com/"; // cámbialo por tu URL real o dominio

export default function Platform() {
  const router = useRouter();

  return (
    <View style={styles.container}>
      <Image source={require("../assets/splash-bg.png")} style={styles.bg} resizeMode="cover" />
      <View style={styles.overlay} />

      <View style={styles.card}>
        <Image source={require("../assets/logo.png")} style={styles.logo} resizeMode="contain" />
        <Text style={styles.title}>Platform Access</Text>
        <Text style={styles.subtitle}>Demo button: opens the NutryGym web platform inside the app.</Text>

        <Pressable
          style={styles.btn}
          onPress={() =>
            router.push({
              pathname: "/webview" as any,
              params: { url: encodeURIComponent(WEB_URL) },
            } as any)
          }

        >
          <Text style={styles.btnText}>Open Platform</Text>
        </Pressable>

        <Text style={styles.note}>If the platform is unavailable, you will see an offline fallback screen.</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0b0b0c", justifyContent: "center", padding: 18 },
  bg: { ...StyleSheet.absoluteFillObject, opacity: 0.45 },
  overlay: { ...StyleSheet.absoluteFillObject, backgroundColor: "rgba(0,0,0,0.60)" },
  card: { backgroundColor: "rgba(255,255,255,0.92)", borderRadius: 18, padding: 18, alignItems: "center" },
  logo: { width: 70, height: 70, marginBottom: 10 },
  title: { fontSize: 26, fontWeight: "900", color: "#111" },
  subtitle: { marginTop: 8, color: "#333", fontWeight: "700", textAlign: "center", lineHeight: 20 },
  btn: { marginTop: 14, width: "100%", backgroundColor: "#80c522", paddingVertical: 14, borderRadius: 12, alignItems: "center" },
  btnText: { color: "white", fontWeight: "900" },
  note: { marginTop: 12, color: "#333", fontWeight: "700", textAlign: "center", fontSize: 12.5 },
});

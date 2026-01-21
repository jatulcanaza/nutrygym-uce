import { useEffect } from "react";
import { View, Image, StyleSheet, Text } from "react-native";
import { useRouter } from "expo-router";

export default function Index() {
  const router = useRouter();

  useEffect(() => {
    const t = setTimeout(() => {
      router.replace("/home" as any);
    }, 3500);

    return () => clearTimeout(t);
  }, [router]);

  return (
    <View style={styles.container}>
      <Image
        source={require("../assets/splash-bg.png")}
        style={styles.bg}
        resizeMode="cover"
      />
      <View style={styles.overlay} />

      <View style={styles.center}>
        <Image
          source={require("../assets/logo.png")}
          style={styles.logo}
          resizeMode="contain"
        />
        <Text style={styles.brand}>NutryGym</Text>
        <Text style={styles.subtitle}>Mobile demo interface</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0b0b0c" },
  bg: { ...StyleSheet.absoluteFillObject, opacity: 0.55 },
  overlay: { ...StyleSheet.absoluteFillObject, backgroundColor: "rgba(0,0,0,0.55)" },
  center: { flex: 1, justifyContent: "center", alignItems: "center", padding: 24 },
  logo: { width: 140, height: 140, marginBottom: 12 },
  brand: { fontSize: 44, fontWeight: "900", color: "white", letterSpacing: 0.5 },
  subtitle: { marginTop: 8, fontSize: 14, color: "rgba(255,255,255,0.75)" },
});

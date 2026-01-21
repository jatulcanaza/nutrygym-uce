import { useEffect } from "react";
import { View, Image, StyleSheet, Text } from "react-native";
import { useRouter } from "expo-router";

export default function Splash() {
  const router = useRouter();

  useEffect(() => {
    const t = setTimeout(() => {
      router.replace("/home");
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
        <Text style={styles.brand}>
          Nutry<Text style={styles.green}>Gym</Text>
        </Text>
        <Text style={styles.subtitle}>Loading demo experience...</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0b0b0c" },
  bg: { ...StyleSheet.absoluteFillObject, opacity: 0.45 },
  overlay: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: "rgba(0,0,0,0.65)",
  },
  center: { flex: 1, justifyContent: "center", alignItems: "center" },
  logo: { width: 120, height: 120, marginBottom: 12 },
  brand: { fontSize: 44, fontWeight: "900", color: "white" },
  green: { color: "#80c522" },
  subtitle: {
    marginTop: 10,
    color: "rgba(255,255,255,0.75)",
    fontWeight: "700",
  },
});

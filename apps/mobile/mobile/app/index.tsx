import { useEffect, useMemo, useRef } from "react";
import { View, Image, StyleSheet, Text, Animated } from "react-native";
import { useRouter } from "expo-router";

export default function Splash() {
  const router = useRouter();

  // Animación de progreso (0 -> 1)
  const progress = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    // Progreso suave durante 3.2s (termina antes del redirect)
    Animated.timing(progress, {
      toValue: 1,
      duration: 3200,
      useNativeDriver: false,
    }).start();

    const t = setTimeout(() => {
      router.replace("/home");
    }, 3500);

    return () => clearTimeout(t);
  }, [router, progress]);

  const progressWidth = useMemo(() => {
    return progress.interpolate({
      inputRange: [0, 1],
      outputRange: ["12%", "100%"],
    });
  }, [progress]);

  return (
    <View style={styles.container}>
      {/* Fondo */}
      <Image
        source={require("../assets/splash-bg.png")}
        style={styles.bg}
        resizeMode="cover"
      />
      <View style={styles.overlay} />

      {/* Contenido */}
      <View style={styles.center}>
        <View style={styles.logoWrap}>
          <Image
            source={require("../assets/logo.png")}
            style={styles.logo}
            resizeMode="contain"
          />
        </View>

        <Text style={styles.brand}>
          Nutry<Text style={styles.green}>Gym</Text>
        </Text>

        <Text style={styles.tagline}>
          Your AI-powered nutrition & training companion
        </Text>

        <Text style={styles.welcome}>
          Welcome back. Preparing your experience…
        </Text>

        {/* Progress bar */}
        <View style={styles.progressTrack}>
          <Animated.View style={[styles.progressFill, { width: progressWidth }]} />
        </View>

        {/* Microcopy inferior */}
        <Text style={styles.hint}>
          Tip: Use the menu to explore demo sections and open the web platform when needed.
        </Text>
      </View>

      {/* Footer */}
      <View style={styles.footer}>
        <Text style={styles.footerText}>NutryGym UCE • Mobile Demo</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0b0b0c" },

  bg: { ...StyleSheet.absoluteFillObject, opacity: 0.40 },
  overlay: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: "rgba(0,0,0,0.72)",
  },

  center: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    paddingHorizontal: 22,
  },

  logoWrap: {
    width: 92,
    height: 92,
    borderRadius: 24,
    backgroundColor: "rgba(255,255,255,0.06)",
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.10)",
    justifyContent: "center",
    alignItems: "center",
    marginBottom: 14,
  },
  logo: { width: 66, height: 66 },

  brand: { fontSize: 44, fontWeight: "900", color: "white" },
  green: { color: "#80c522" },

  tagline: {
    marginTop: 6,
    color: "rgba(255,255,255,0.78)",
    fontWeight: "700",
    textAlign: "center",
  },

  welcome: {
    marginTop: 18,
    color: "rgba(255,255,255,0.86)",
    fontWeight: "800",
    textAlign: "center",
  },

  progressTrack: {
    marginTop: 18,
    width: "78%",
    height: 10,
    borderRadius: 999,
    backgroundColor: "rgba(255,255,255,0.10)",
    overflow: "hidden",
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.08)",
  },
  progressFill: {
    height: "100%",
    borderRadius: 999,
    backgroundColor: "#80c522",
  },

  hint: {
    marginTop: 18,
    maxWidth: 360,
    textAlign: "center",
    color: "rgba(255,255,255,0.62)",
    fontWeight: "700",
    lineHeight: 18,
    fontSize: 12.5,
  },

  footer: {
    paddingBottom: 18,
    paddingTop: 10,
    alignItems: "center",
  },
  footerText: {
    color: "rgba(255,255,255,0.55)",
    fontWeight: "700",
    fontSize: 12,
  },
});

import { View, Text, StyleSheet, Pressable } from "react-native";
import { useLocalSearchParams, useRouter } from "expo-router";
import { WebView } from "react-native-webview";

const DEFAULT_URL =
  "http://nutrygym-uce-qa-alb-1894441400.us-east-1.elb.amazonaws.com/";

export default function WebViewScreen() {
  const router = useRouter();
  const params = useLocalSearchParams<{ url?: string | string[] }>();

  // 1) Normalizar: string | string[] | undefined  -> string | undefined
  const rawUrl = Array.isArray(params.url) ? params.url[0] : params.url;

  // 2) Decodificar si viene codificada
  let finalUrl = DEFAULT_URL;
  if (rawUrl && typeof rawUrl === "string") {
    try {
      finalUrl = decodeURIComponent(rawUrl);
    } catch {
      finalUrl = rawUrl; // si no estaba codificada
    }
  }

  return (
    <View style={styles.container}>
      <View style={styles.topBar}>
        {/* Mejor que replace("/home") para que funcione desde cualquier lugar */}
        <Pressable style={styles.backBtn} onPress={() => router.back()}>
          <Text style={styles.backText}>← Back</Text>
        </Pressable>

        <Text style={styles.topTitle}>NutryGym Platform</Text>
      </View>

      <WebView
        source={{ uri: finalUrl }}
        originWhitelist={["*"]}
        mixedContentMode="always"
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0b0b0c" },
  topBar: {
    height: 56,
    backgroundColor: "#0b0b0c",
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 12,
  },
  backBtn: {
    paddingHorizontal: 12,
    paddingVertical: 10,
    borderRadius: 12,
    backgroundColor: "rgba(255,255,255,0.08)",
  },
  backText: { color: "white", fontWeight: "900" },
  topTitle: { marginLeft: 12, color: "white", fontWeight: "900", fontSize: 16 },
});

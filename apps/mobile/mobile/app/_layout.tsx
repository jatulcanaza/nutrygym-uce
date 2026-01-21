import { Drawer } from "expo-router/drawer";

export default function RootLayout() {
  return (
    <Drawer
      screenOptions={{
        headerStyle: { backgroundColor: "#0b0b0c" },
        headerTintColor: "#fff",
        drawerStyle: { backgroundColor: "#0b0b0c" },
        drawerActiveTintColor: "#80c522",
        drawerInactiveTintColor: "rgba(255,255,255,0.8)",
      }}
    >
      {/* Ocultamos index (Splash) del menú */}
      <Drawer.Screen name="index" options={{ drawerItemStyle: { display: "none" }, headerShown: false }} />

      <Drawer.Screen name="home" options={{ title: "Home" }} />
      <Drawer.Screen name="about" options={{ title: "About" }} />
      <Drawer.Screen name="plans" options={{ title: "Plans" }} />
      <Drawer.Screen name="platform" options={{ title: "Web Platform" }} />
      <Drawer.Screen name="app-info" options={{ title: "App Info" }} />

      {/* Ocultamos webview del menú (se abre desde botón, no desde menú) */}
      <Drawer.Screen name="webview" options={{ drawerItemStyle: { display: "none" }, title: "NutryGym Platform" }} />
    </Drawer>
  );
}

import { Routes, Route } from "react-router-dom";
import Welcome from "../pages/Welcome";
import About from "../pages/About";
import Plans from "../pages/Plans";
import NutriGym from "../pages/NutriGym";
import Auth from "../pages/Auth";
import NutritionForm from "../pages/NutritionForm";

export default function AppRouter() {
  return (
    <Routes>
      <Route path="/" element={<Welcome />} />
      <Route path="/about" element={<About />} />
      <Route path="/plans" element={<Plans />} />
      <Route path="/nutrigym" element={<NutriGym />} />
      <Route path="/auth" element={<Auth />} />
      <Route path="/nutrition-form" element={<NutritionForm />} />
    </Routes>
  );
}

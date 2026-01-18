import { useEffect, useMemo, useState } from "react";
import { useAuth } from "../context/AuthContext";
import "./NutriGym.css";
import { getMyProfile, createProfile, updateMyProfile } from "../api/profile.api";



// Recomendado: coloca la imagen en public y usa /nutrition-hero.png
// Si sí la tienes en src/assets, puedes volver a importarla.
// const HERO_IMG = "/nutrition-hero.png";
const HERO_IMG = "/src/assets/nutrition-hero.png";

type Gender = "male" | "female" | "other";
type Goal = "lose_weight" | "gain_muscle" | "maintain";
type Activity = "low" | "moderate" | "high";

type ProfileForm = {
  first_name: string;
  last_name: string;
  birth_date: string; // YYYY-MM-DD
  gender: "" | Gender;
  height_cm: string; // input text -> luego number
  weight_kg: string;
  goal: "" | Goal;
  activity_level: "" | Activity;
};

type NutritionForm = {
  preferences: string;
  allergies: string;
  mealsPerDay: "" | "3" | "4" | "5";
  budget: "" | "low" | "medium" | "high";
};

type Plan = {
  goalLabel: string;
  week: Record<string, [string, string, string]>;
  conclusion: string;
  status: "Active" | "Canceled";
  createdAt: string; // locale
};

export default function NutriGym() {
 const { user, token, isAuthenticated, logout } = useAuth();


  // ====== UI state
  const [showProfileModal, setShowProfileModal] = useState(false);
  const [showNutritionModal, setShowNutritionModal] = useState(false);

  // simula "perfil existe"; luego lo reemplazas por GET /profiles/me
const [hasProfile, setHasProfile] = useState<boolean | null>(null);
const [loadingProfile, setLoadingProfile] = useState(true);

  // ====== Forms
  const [profileForm, setProfileForm] = useState<ProfileForm>({
    first_name: "",
    last_name: "",
    birth_date: "",
    gender: "",
    height_cm: "",
    weight_kg: "",
    goal: "",
    activity_level: "",
  });

  const [nutritionForm, setNutritionForm] = useState<NutritionForm>({
    preferences: "",
    allergies: "",
    mealsPerDay: "",
    budget: "",
  });

  // ====== Errors
  const [profileErrors, setProfileErrors] = useState<Record<string, string>>({});
  const [nutritionErrors, setNutritionErrors] = useState<Record<string, string>>({});

  // ====== Plan state
  const [plan, setPlan] = useState<Plan | null>(null);
  const [history, setHistory] = useState<Array<Pick<Plan, "createdAt" | "goalLabel" | "status">>>([]);

  // ====== Scroll lock cuando modal abierto
  useEffect(() => {
  const open = showProfileModal || showNutritionModal;
  document.body.style.overflow = open ? "hidden" : "auto";
  return () => {
    document.body.style.overflow = "auto";
  };
}, [showProfileModal, showNutritionModal]);
  // ====== Chequea si el perfil existe al montar
useEffect(() => {
  if (!token) return;

  const checkProfile = async () => {
    try {
      const profile = await getMyProfile(token);

      // ✅ Perfil existe
      setHasProfile(true);

      // ✅ Precargar el formulario con lo que viene del backend
      setProfileForm({
        first_name: profile.first_name,
        last_name: profile.last_name,
        birth_date: profile.birth_date,
        gender: profile.gender as any,
        height_cm: String(profile.height_cm),
        weight_kg: String(profile.weight_kg),
        goal: profile.goal as any,
        activity_level: profile.activity_level as any,
      });
    } catch (err: any) {
      if (err?.response?.status === 404) {
        setHasProfile(false); // no existe
      } else {
        console.error("Error checking profile", err);
      }
    } finally {
      setLoadingProfile(false);
    }
  };

  checkProfile();
}, [token]);


  // ====== Helpers
  const username = useMemo(() => {
    const email = user?.email ?? "";
    return email.includes("@") ? email.split("@")[0] : "user";
  }, [user?.email]);

const openFlow = () => {
  if (loadingProfile) return;

  if (!hasProfile) {
    setShowProfileModal(true);
  } else {
    setShowNutritionModal(true);
  }
};


  // ====== Validaciones
  const validateProfile = (data: ProfileForm) => {
    const e: Record<string, string> = {};

    if (!data.first_name.trim()) e.first_name = "First name is required.";
    if (!data.last_name.trim()) e.last_name = "Last name is required.";
    if (!data.birth_date) e.birth_date = "Birth date is required.";
    if (!data.gender) e.gender = "Gender is required.";

    const h = Number(data.height_cm);
    const w = Number(data.weight_kg);
    if (!data.height_cm.trim() || Number.isNaN(h)) e.height_cm = "Height must be a number.";
    else if (h < 80 || h > 250) e.height_cm = "Height must be between 80 and 250 cm.";

    if (!data.weight_kg.trim() || Number.isNaN(w)) e.weight_kg = "Weight must be a number.";
    else if (w < 20 || w > 300) e.weight_kg = "Weight must be between 20 and 300 kg.";

    if (!data.goal) e.goal = "Goal is required.";
    if (!data.activity_level) e.activity_level = "Activity level is required.";

    setProfileErrors(e);
    return Object.keys(e).length === 0;
  };

  const validateNutrition = (data: NutritionForm) => {
    const e: Record<string, string> = {};
    if (!data.preferences.trim()) e.preferences = "Preferences are required.";
    // alergias pueden ser opcionales
    if (!data.mealsPerDay) e.mealsPerDay = "Select meals per day.";
    if (!data.budget) e.budget = "Select budget.";
    setNutritionErrors(e);
    return Object.keys(e).length === 0;
  };

  // ====== Acciones de perfil
const handleProfileNext = async () => {
  if (!validateProfile(profileForm)) return;
  if (!token) return;

  const payload = {
    first_name: profileForm.first_name,
    last_name: profileForm.last_name,
    birth_date: profileForm.birth_date,
    gender: profileForm.gender,
    height_cm: Number(profileForm.height_cm),
    weight_kg: Number(profileForm.weight_kg),
    goal: profileForm.goal,
    activity_level: profileForm.activity_level,
  };

  try {
    // ✅ Si NO existe perfil -> POST
    if (!hasProfile) {
      await createProfile(token, payload);
      setHasProfile(true);
    } else {
      // ✅ Si YA existe -> PUT (update)
      await updateMyProfile(token, payload);
    }

    setShowProfileModal(false);
    setShowNutritionModal(true);
  } catch (err: any) {
    // Si backend responde "ya existe" al intentar crear, abrimos nutrition
    if (err?.response?.status === 409) {
      setHasProfile(true);
      setShowProfileModal(false);
      setShowNutritionModal(true);
      return;
    }

    console.error("Error saving profile", err);
    alert("Failed to save profile. Please try again.");
  }
};



  // ====== Acciones de nutrición/plan
  const handleGeneratePlan = () => {
    if (!validateNutrition(nutritionForm)) return;

    // Aquí luego conectas a IA + nutrition-form-service
    const generated: Plan = {
      goalLabel:
        profileForm.goal === "lose_weight"
          ? "Lose weight"
          : profileForm.goal === "gain_muscle"
          ? "Gain muscle"
          : "Maintain",
      week: {
        Monday: ["Oatmeal", "Chicken salad", "Fruit"],
        Tuesday: ["Eggs", "Rice & fish", "Yogurt"],
        Wednesday: ["Smoothie", "Pasta", "Nuts"],
        Thursday: ["Toast", "Chicken & veggies", "Fruit"],
        Friday: ["Oats", "Fish & rice", "Yogurt"],
        Saturday: ["Eggs", "Salad", "Fruit"],
        Sunday: ["Free choice", "Balanced meal", "Light snack"],
      },
      conclusion:
        "This plan is personalized based on your profile and habits. Follow it consistently and adjust portions according to your progress.",
      status: "Active",
      createdAt: new Date().toLocaleDateString(),
    };

    setPlan(generated);
    setHistory((prev) => [{ createdAt: generated.createdAt, goalLabel: generated.goalLabel, status: generated.status }, ...prev]);
    setShowNutritionModal(false);
  };

  const handleEditPlan = () => {
    // Reabre SOLO nutrition form (con datos actuales)
    setShowNutritionModal(true);
  };

  const handleCancelPlan = () => {
    if (!plan) return;
    const canceled = { ...plan, status: "Canceled" as const };

    setPlan(null); // el plan activo desaparece
    // actualiza historial con cancelado
    setHistory((prev) => {
      const updated = [...prev];
      const idx = updated.findIndex((x) => x.createdAt === canceled.createdAt && x.goalLabel === canceled.goalLabel);
      if (idx >= 0) updated[idx] = { ...updated[idx], status: "Canceled" };
      else updated.unshift({ createdAt: canceled.createdAt, goalLabel: canceled.goalLabel, status: "Canceled" });
      return updated;
    });
  };

  // ====== UX: cerrar modal con Escape + click fuera
  const onOverlayClick = (close: () => void) => (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) close();
  };

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        setShowProfileModal(false);
        setShowNutritionModal(false);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  return (
    <section className="nutrigym-page">
      {/* HERO */}
      <div className="nutrigym-hero">
        <div className="hero-text">
          <div className="hero-kicker">NutryGym Dashboard</div>

          <h1 className="hero-title">
            Welcome <span className="green">{username}</span>
          </h1>

          <p className="hero-subtitle">
            Build a personalized weekly plan powered by AI. Start by completing your profile, then submit your nutrition preferences.
          </p>

          <div className="hero-actions">
            <button
              className="btn btn-primary"
              onClick={openFlow}
              disabled={loadingProfile}
            >
              {loadingProfile ? "Loading..." : "Get my nutrition plan"}
            </button>


            {isAuthenticated && (
              <button className="btn btn-ghost" onClick={logout} type="button">
                Log out
              </button>
            )}
          </div>
        </div>

        <div className="hero-media">
          <img src={HERO_IMG} alt="Nutrition illustration" className="hero-img" />
        </div>
      </div>

      {/* HOW IT WORKS */}
      <div className="how-it-works">
        <div className="section-title">
          <h2>How it works</h2>
          <p>Follow the guided flow. You can go back anytime to adjust your data.</p>
        </div>

        <div className="steps">
          <div className="step">
            <div className="step-title">1. Profile</div>
            <div className="step-desc">Height, weight, goal, and activity level.</div>
          </div>
          <div className="step">
            <div className="step-title">2. Nutrition form</div>
            <div className="step-desc">Preferences, allergies, meals per day, budget.</div>
          </div>
          <div className="step">
            <div className="step-title">3. AI generation</div>
            <div className="step-desc">Weekly plan Monday–Sunday with meals.</div>
          </div>
          <div className="step">
            <div className="step-title">4. Manage</div>
            <div className="step-desc">Edit, cancel, and keep history.</div>
          </div>
        </div>
      </div>

      {/* PLAN */}
      {plan && (
        <div className="panel">
          <div className="panel-header">
            <div>
              <h2>Your weekly plan</h2>
              <p className="muted">Goal: {plan.goalLabel} • Status: {plan.status} • Created: {plan.createdAt}</p>
            </div>

            <div className="panel-actions">
              <button className="btn btn-primary" type="button" onClick={handleEditPlan}>
                Edit plan
              </button>
              <button className="btn btn-danger" type="button" onClick={handleCancelPlan}>
                Cancel plan
              </button>
            </div>
          </div>

          <div className="table-wrap">
            <table className="plan-table">
              <thead>
                <tr>
                  <th>Day</th>
                  <th>Breakfast</th>
                  <th>Lunch</th>
                  <th>Snack</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(plan.week).map(([day, meals]) => (
                  <tr key={day}>
                    <td className="day">{day}</td>
                    <td>{meals[0]}</td>
                    <td>{meals[1]}</td>
                    <td>{meals[2]}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="ai-box">
            <div className="ai-title">AI conclusion</div>
            <p>{plan.conclusion}</p>
          </div>
        </div>
      )}

      {/* HISTORY */}
      <div className="panel">
        <div className="panel-header">
          <div>
            <h2>Plan history</h2>
            <p className="muted">All generated plans are recorded with their status.</p>
          </div>
        </div>

        {history.length === 0 ? (
          <div className="empty">
            No plans yet. Click “Get my nutrition plan” to generate your first plan.
          </div>
        ) : (
          <div className="table-wrap">
            <table className="history-table">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Goal</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {history.map((h, i) => (
                  <tr key={i}>
                    <td>{h.createdAt}</td>
                    <td>{h.goalLabel}</td>
                    <td>
                      <span className={`badge ${h.status === "Active" ? "badge-active" : "badge-canceled"}`}>
                        {h.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* PROFILE MODAL */}
      {showProfileModal && (
        <div className="modal-overlay" role="dialog" aria-modal="true" onClick={onOverlayClick(() => setShowProfileModal(false))}>
          <div className="modal-card">
            <div className="modal-header">
              <div>
                <h3>Create user profile</h3>
                <p className="modal-subtitle">This is required before generating your nutrition plan.</p>
              </div>
              <button className="modal-close" type="button" onClick={() => setShowProfileModal(false)} aria-label="Close">
                ×
              </button>
            </div>

            <div className="modal-body">
              <div className="modal-grid">
                <div className="field">
                  <label>First name</label>
                  <input
                    value={profileForm.first_name}
                    onChange={(e) => setProfileForm({ ...profileForm, first_name: e.target.value })}
                    placeholder="First name"
                  />
                  {profileErrors.first_name && <small className="error">{profileErrors.first_name}</small>}
                </div>

                <div className="field">
                  <label>Last name</label>
                  <input
                    value={profileForm.last_name}
                    onChange={(e) => setProfileForm({ ...profileForm, last_name: e.target.value })}
                    placeholder="Last name"
                  />
                  {profileErrors.last_name && <small className="error">{profileErrors.last_name}</small>}
                </div>

                <div className="field">
                  <label>Birth date</label>
                  <input
                    type="date"
                    value={profileForm.birth_date}
                    onChange={(e) => setProfileForm({ ...profileForm, birth_date: e.target.value })}
                  />
                  {profileErrors.birth_date && <small className="error">{profileErrors.birth_date}</small>}
                </div>

                <div className="field">
                  <label>Gender</label>
                  <select
                    value={profileForm.gender}
                    onChange={(e) => setProfileForm({ ...profileForm, gender: e.target.value as any })}
                  >
                    <option value="" disabled>Select gender</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                  </select>
                  {profileErrors.gender && <small className="error">{profileErrors.gender}</small>}
                </div>

                <div className="field">
                  <label>Height (cm)</label>
                  <input
                    type="number"
                    value={profileForm.height_cm}
                    onChange={(e) => setProfileForm({ ...profileForm, height_cm: e.target.value })}
                    placeholder="e.g. 170"
                  />
                  {profileErrors.height_cm && <small className="error">{profileErrors.height_cm}</small>}
                </div>

                <div className="field">
                  <label>Weight (kg)</label>
                  <input
                    type="number"
                    value={profileForm.weight_kg}
                    onChange={(e) => setProfileForm({ ...profileForm, weight_kg: e.target.value })}
                    placeholder="e.g. 70"
                  />
                  {profileErrors.weight_kg && <small className="error">{profileErrors.weight_kg}</small>}
                </div>

                <div className="field">
                  <label>Goal</label>
                  <select
                    value={profileForm.goal}
                    onChange={(e) => setProfileForm({ ...profileForm, goal: e.target.value as any })}
                  >
                    <option value="" disabled>Select goal</option>
                    <option value="lose_weight">Lose weight</option>
                    <option value="gain_muscle">Gain muscle</option>
                    <option value="maintain">Maintain</option>
                  </select>
                  {profileErrors.goal && <small className="error">{profileErrors.goal}</small>}
                </div>

                <div className="field">
                  <label>Activity level</label>
                  <select
                    value={profileForm.activity_level}
                    onChange={(e) => setProfileForm({ ...profileForm, activity_level: e.target.value as any })}
                  >
                    <option value="" disabled>Select activity level</option>
                    <option value="low">Low</option>
                    <option value="moderate">Moderate</option>
                    <option value="high">High</option>
                  </select>
                  {profileErrors.activity_level && <small className="error">{profileErrors.activity_level}</small>}
                </div>
              </div>
            </div>

            <div className="modal-footer">
              <button className="btn btn-ghost" type="button" onClick={() => setShowProfileModal(false)}>
                Cancel
              </button>
              <button className="btn btn-primary" type="button" onClick={handleProfileNext}>
                Continue
              </button>
            </div>
          </div>
        </div>
      )}

      {/* NUTRITION MODAL */}
      {showNutritionModal && (
        <div className="modal-overlay" role="dialog" aria-modal="true" onClick={onOverlayClick(() => setShowNutritionModal(false))}>
          <div className="modal-card">
            <div className="modal-header">
              <div>
                <h3>Nutrition form</h3>
                <p className="modal-subtitle">Review your profile if you need. Then generate your weekly plan.</p>
              </div>
              <button className="modal-close" type="button" onClick={() => setShowNutritionModal(false)} aria-label="Close">
                ×
              </button>
            </div>

            <div className="modal-body">
              <div className="modal-grid">
                <div className="field full">
                  <label>Food preferences</label>
                  <input
                    value={nutritionForm.preferences}
                    onChange={(e) => setNutritionForm({ ...nutritionForm, preferences: e.target.value })}
                    placeholder="e.g. vegetarian, no seafood"
                  />
                  {nutritionErrors.preferences && <small className="error">{nutritionErrors.preferences}</small>}
                </div>

                <div className="field full">
                  <label>Allergies (optional)</label>
                  <input
                    value={nutritionForm.allergies}
                    onChange={(e) => setNutritionForm({ ...nutritionForm, allergies: e.target.value })}
                    placeholder="e.g. lactose, peanuts"
                  />
                </div>

                <div className="field">
                  <label>Meals per day</label>
                  <select
                    value={nutritionForm.mealsPerDay}
                    onChange={(e) => setNutritionForm({ ...nutritionForm, mealsPerDay: e.target.value as any })}
                  >
                    <option value="" disabled>Select</option>
                    <option value="3">3</option>
                    <option value="4">4</option>
                    <option value="5">5</option>
                  </select>
                  {nutritionErrors.mealsPerDay && <small className="error">{nutritionErrors.mealsPerDay}</small>}
                </div>

                <div className="field">
                  <label>Budget</label>
                  <select
                    value={nutritionForm.budget}
                    onChange={(e) => setNutritionForm({ ...nutritionForm, budget: e.target.value as any })}
                  >
                    <option value="" disabled>Select</option>
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>
                  {nutritionErrors.budget && <small className="error">{nutritionErrors.budget}</small>}
                </div>
              </div>

              <p className="modal-hint">
                Tip: You can go back to edit your profile if something is incorrect.
              </p>
            </div>

            <div className="modal-footer">
              <button className="btn btn-ghost" type="button" onClick={() => setShowNutritionModal(false)}>
                Cancel
              </button>
              <button
                className="btn btn-primary"
                type="button"
                onClick={() => {
                  setShowNutritionModal(false);
                  setShowProfileModal(true);
                }}
              >
                Back to profile
              </button>
              <button className="btn btn-primary" type="button" onClick={handleGeneratePlan}>
                Generate plan
              </button>
            </div>
          </div>
        </div>
      )}
    </section>
  );
}

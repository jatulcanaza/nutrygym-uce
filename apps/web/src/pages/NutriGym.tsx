import { useEffect, useMemo, useRef, useState } from "react";
import { useAuth } from "../context/AuthContext";
import "./NutriGym.css";
import { getMyProfile, createProfile, updateMyProfile } from "../api/profile.api";
import {
  getMyNutritionForm,
  createNutritionForm,
  updateMyNutritionForm,
} from "../api/nutritionForm.api";
import {
  getCurrentPlan,
  regenerateCurrentPlan,
  generatePlan,
  getMyPlans,
  endPlan,
  cancelPlan,
  type MealPlan
} from "../api/plan.api";


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

type DietType = "low" | "medium" | "high"; // ajustable si quieres texto libre

type NutritionForm = {
  meals_per_day: "" | "3" | "4" | "5";     // lo guardamos como string para el select
  diet_type: "" | DietType;

  allergies: string;       // input texto -> luego a array
  preferences: string;     // input texto -> luego a array

  caloric_goal: string;    // input texto -> luego number
  water_intake: string;    // input texto -> luego number
};


type Plan = MealPlan;

type PlanJSON = {
  title: string;
  summary?: string;
  macros: { calories: number; protein_g: number; carbs_g: number; fats_g: number };
  week: { day: string; meals: { type: string; name: string; notes?: string }[] }[];
  tips?: string[];
};

export default function NutriGym() {
  const { user, token, isAuthenticated, logout } = useAuth();


  // ====== UI state
  const [showProfileModal, setShowProfileModal] = useState(false);
  const [showNutritionModal, setShowNutritionModal] = useState(false);
  const [plans, setPlans] = useState<MealPlan[]>([]);
  const [loadingPlans, setLoadingPlans] = useState(true);
  const [generating, setGenerating] = useState(false);
  const generatingRef = useRef(false);
  const [editingPlan, setEditingPlan] = useState(false);



  // simula "perfil existe"; luego lo reemplazas por GET /profiles/me
  const [hasProfile, setHasProfile] = useState<boolean | null>(null);
  const [loadingProfile, setLoadingProfile] = useState(true);
  const [hasNutritionForm, setHasNutritionForm] = useState<boolean | null>(null);
  const [loadingNutritionForm, setLoadingNutritionForm] = useState(true);


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
    meals_per_day: "",
    diet_type: "",
    allergies: "",
    preferences: "",
    caloric_goal: "",
    water_intake: "",
  });

  // ====== Errors
  const [profileErrors, setProfileErrors] = useState<Record<string, string>>({});
  const [nutritionErrors, setNutritionErrors] = useState<Record<string, string>>({});

  // ====== Plan state
  const [plan, setPlan] = useState<Plan | null>(null);
  const planJson: PlanJSON | null = useMemo(() => {
  if (!plan?.description) return null;
  try {
    return JSON.parse(plan.description);
  } catch {
    return null;
  }
}, [plan?.description]);


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

  useEffect(() => {
    if (!token) return;

    const checkNutritionForm = async () => {
      try {
        const nf = await getMyNutritionForm(token);

        setHasNutritionForm(true);

        setNutritionForm({
          meals_per_day: String(nf.meals_per_day) as any,
          diet_type: nf.diet_type as any,
          allergies: (nf.allergies ?? []).join(", "),
          preferences: (nf.preferences ?? []).join(", "),
          caloric_goal: String(nf.caloric_goal),
          water_intake: String(nf.water_intake),
        });
      } catch (err: any) {
        if (err?.response?.status === 404) {
          setHasNutritionForm(false);
        } else {
          console.error("Error checking nutrition form", err);
        }
      } finally {
        setLoadingNutritionForm(false);
      }
    };

    checkNutritionForm();
  }, [token]);
  useEffect(() => {
    if (!token) return;

    const loadCurrentPlan = async () => {
      try {
        const p = await getCurrentPlan(token);
        setPlan(p);
      } catch (err: any) {
        if (err?.response?.status === 404) {
          setPlan(null); // ✅ IMPORTANTE: limpia estado local
        } else {
          console.error("Error loading current plan", err);
        }
      }
    };

    loadCurrentPlan();
  }, [token]);


  useEffect(() => {
    if (!token) return;
    refreshPlans();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token]);


  // ====== Helpers
  const username = useMemo(() => {
    const email = user?.email ?? "";
    return email.includes("@") ? email.split("@")[0] : "user";
  }, [user?.email]);

  const openFlow = () => {
    if (loadingProfile || loadingNutritionForm) return;

    // ✅ Si ya hay plan activo, no abras modales
    if (plan) return;

    if (!hasProfile) setShowProfileModal(true);
    else setShowNutritionModal(true);
  };

  const refreshPlans = async () => {
    if (!token) return;

    try {
      setLoadingPlans(true);
      const list = await getMyPlans(token);

      // Ordena por fecha (más nuevo primero)
      const sorted = [...list].sort(
        (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      );

      setPlans(sorted);

      // ❌ NO vuelvas a setear `plan` desde el historial.
      // La única fuente de verdad del plan activo es GET /plans/current
    } catch (err: any) {
      console.error("Error loading plans", err);
    } finally {
      setLoadingPlans(false);
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

    if (!data.diet_type) e.diet_type = "Select diet type.";
    if (!data.meals_per_day) e.meals_per_day = "Select meals per day.";

    // preferences lo hacemos requerido (como tenías)
    if (!data.preferences.trim()) e.preferences = "Preferences are required.";

    // caloric_goal y water_intake requeridos
    const cg = Number(data.caloric_goal);
    if (!data.caloric_goal.trim() || Number.isNaN(cg) || cg <= 0) {
      e.caloric_goal = "Caloric goal must be a positive number.";
    }

    const wi = Number(data.water_intake);
    if (!data.water_intake.trim() || Number.isNaN(wi) || wi <= 0) {
      e.water_intake = "Water intake must be a positive number.";
    }

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
  const handleGeneratePlan = async () => {
    if (generatingRef.current) return; // ✅ lock real
    if (!validateNutrition(nutritionForm)) return;
    if (!token) return;

    generatingRef.current = true;
    setGenerating(true);


    const parseList = (s: string) =>
      s
        .split(",")
        .map((x) => x.trim())
        .filter(Boolean);

    const payload = {
      meals_per_day: Number(nutritionForm.meals_per_day),
      diet_type: nutritionForm.diet_type,
      allergies: parseList(nutritionForm.allergies),
      preferences: parseList(nutritionForm.preferences),
      caloric_goal: Number(nutritionForm.caloric_goal),
      water_intake: Number(nutritionForm.water_intake),
    };

    try {
      // 1️⃣ Guarda / actualiza nutrition form
      if (!hasNutritionForm) {
        await createNutritionForm(token, payload);
        setHasNutritionForm(true);
      } else {
        await updateMyNutritionForm(token, payload);
      }

      // 2️⃣ Genera el plan REAL
      let newPlan: MealPlan;

      if (plan && editingPlan) {
        // Editar = regenerar plan actual
        newPlan = await regenerateCurrentPlan(token);
      } else {
        // Nuevo = generar plan
        newPlan = await generatePlan(token);
      }

      setPlan(newPlan);
      setEditingPlan(false);


      setShowNutritionModal(false);
      await refreshPlans();

    } catch (err: any) {
      if (err?.response?.status === 409) {
        alert("You already have an active plan. End or cancel it first.");
        return;
      }
      console.error("Error generating plan", err);
      alert("Failed to generate plan. Please try again.");
    } finally {
      setGenerating(false);
      generatingRef.current = false;
    }


  };


  const handleEditPlan = () => {
    setEditingPlan(true);
    setShowNutritionModal(true);
  };


  const handleEndPlan = async () => {
    if (!token || !plan) return;

    const ok = window.confirm("Do you want to end this plan?");
    if (!ok) return;

    try {
      await endPlan(token);

      setPlan(null);
      await refreshPlans();
      try {
        await getCurrentPlan(token);
      } catch (e: any) {
        // si es 404, perfecto, no hay plan activo
      }

    } catch (err: any) {
      console.error("Error ending plan", err);
      alert("Failed to end plan. Please try again.");
    }
  };



  const handleCancelPlan = async () => {
    if (!token || !plan) return;

    const ok = window.confirm("Do you want to cancel this plan?");
    if (!ok) return;

    try {
      await cancelPlan(token);

      setPlan(null);
      await refreshPlans();
      try {
        await getCurrentPlan(token);
      } catch (e: any) {
        // si es 404, perfecto, no hay plan activo
      }

    } catch (err: any) {
      console.error("Error canceling plan", err);
      alert("Failed to cancel plan. Please try again.");
    }
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
              disabled={loadingProfile || loadingNutritionForm}>
              {(loadingProfile || loadingNutritionForm) ? "Loading..." : "Get my nutrition plan"}

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
            <div className="step-desc">Preferences, allergies, meals per day, diet type, calories, water.</div>
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
              <h2>{plan.title}</h2>
              <p className="muted">
                Status: {plan.status} • Version: {plan.version} • Created:{" "}
                {new Date(plan.created_at).toLocaleString()}
              </p>
            </div>

            <div className="panel-actions">
              <button className="btn btn-primary" type="button" onClick={handleEditPlan}>
                Edit nutrition form
              </button>
              <button className="btn btn-danger" type="button" onClick={handleEndPlan}>
                End plan
              </button>
              <button className="btn btn-ghost" type="button" onClick={handleCancelPlan}>
                Cancel plan
              </button>
            </div>
          </div>

        {/* <div className="ai-box">
            <div className="ai-title">Macros</div>
            <p>
              Calories: {planJson?.macros?.calories ?? plan.calories} •
              Protein: {planJson?.macros?.protein_g ?? plan.protein}g •
              Carbs: {planJson?.macros?.carbs_g ?? plan.carbs}g •
              Fats: {planJson?.macros?.fats_g ?? plan.fats}g
            </p>
          </div>*/}

         <div className="ai-box">
  <div className="ai-title">Plan details</div>

  {planJson ? (
    <>
      {planJson.summary && <p className="plan-summary">{planJson.summary}</p>}

      <div className="week-grid">
        {planJson.week.map((d) => (
          <div key={d.day} className="day-card">
            <div className="day-card-head">
            <div className="day-card-title">{d.day}</div>
            <span className="day-chip">{d.meals.length} meals</span>
          </div>


            <div className="meals">
              {d.meals.map((m, idx) => (
                <div key={idx} className="meal-row">
                  <span className={`meal-type pill pill-${m.type.toLowerCase()}`}>
                      {m.type}
                    </span>

                  <div className="meal-main">
                    <div className="meal-name">{m.name}</div>
                    {m.notes && <div className="meal-notes">{m.notes}</div>}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {planJson.tips?.length ? (
        <div className="tips-box">
          <div className="tips-title">Tips</div>
          <ul>
            {planJson.tips.map((t, i) => <li key={i}>{t}</li>)}
          </ul>
        </div>
      ) : null}
    </>
  ) : (
    <pre style={{ whiteSpace: "pre-wrap", margin: 0 }}>{plan.description}</pre>
  )}
</div>



        </div>
      )}


      {/* PLAN HISTORY */}
      <div className="panel">
        <div className="panel-header">
          <div>
            <h2>Plan history</h2>
            <p className="muted">All your generated plans (active and archived).</p>
          </div>
        </div>

        {loadingPlans ? (
          <div className="empty">Loading plans...</div>
        ) : plans.length === 0 ? (
          <div className="empty">
            No plans yet. Click “Get my nutrition plan” to generate your first plan.
          </div>
        ) : (
          <div className="table-wrap">
            <table className="history-table">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Title</th>
                  <th>Status</th>
                  <th>Current</th>
                </tr>
              </thead>
              <tbody>
                {plans.map((p) => (
                  <tr key={p.id}>
                    <td>{new Date(p.created_at).toLocaleString()}</td>
                    <td>{p.title}</td>
                    <td>
                      <span className={`badge ${p.status === "active" ? "badge-active" : "badge-canceled"}`}>
                        {p.status}
                      </span>
                    </td>
                    <td>{p.is_current ? "Yes" : "No"}</td>
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
              <button
                className="modal-close"
                type="button"
                onClick={() => {
                  setShowProfileModal(false);
                }}
                aria-label="Close"
              >
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
              <button
                className="btn btn-ghost"
                type="button"
                onClick={() => {
                  setShowProfileModal(false);
                }}
              >
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
              <button
                className="modal-close"
                type="button"
                onClick={() => {
                  setShowNutritionModal(false);
                }}
                aria-label="Close"
              >
                ×
              </button>

            </div>

            <div className="modal-body">
              <div className="modal-grid">
                <div className="field full">
                  <label>Food preferences</label>
                  <input
                    value={nutritionForm.preferences}
                    onChange={(e) =>
                      setNutritionForm({ ...nutritionForm, preferences: e.target.value })
                    }
                    placeholder="e.g. vegetarian, no seafood"
                  />
                  {nutritionErrors.preferences && (
                    <small className="error">{nutritionErrors.preferences}</small>
                  )}
                </div>

                <div className="field full">
                  <label>Allergies (optional)</label>
                  <input
                    value={nutritionForm.allergies}
                    onChange={(e) =>
                      setNutritionForm({ ...nutritionForm, allergies: e.target.value })
                    }
                    placeholder="e.g. lactose, peanuts"
                  />
                </div>

                <div className="field">
                  <label>Meals per day</label>
                  <select
                    value={nutritionForm.meals_per_day}
                    onChange={(e) =>
                      setNutritionForm({ ...nutritionForm, meals_per_day: e.target.value as any })
                    }
                  >
                    <option value="" disabled>Select</option>
                    <option value="3">3</option>
                    <option value="4">4</option>
                    <option value="5">5</option>
                  </select>
                  {nutritionErrors.meals_per_day && (
                    <small className="error">{nutritionErrors.meals_per_day}</small>
                  )}
                </div>

                <div className="field">
                  <label>Diet type</label>
                  <select
                    value={nutritionForm.diet_type}
                    onChange={(e) =>
                      setNutritionForm({ ...nutritionForm, diet_type: e.target.value as any })
                    }
                  >
                    <option value="" disabled>Select</option>
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>
                  {nutritionErrors.diet_type && (
                    <small className="error">{nutritionErrors.diet_type}</small>
                  )}
                </div>

                <div className="field">
                  <label>Caloric goal</label>
                  <input
                    type="number"
                    value={nutritionForm.caloric_goal}
                    onChange={(e) =>
                      setNutritionForm({ ...nutritionForm, caloric_goal: e.target.value })
                    }
                    placeholder="e.g. 2200"
                  />
                  {nutritionErrors.caloric_goal && (
                    <small className="error">{nutritionErrors.caloric_goal}</small>
                  )}
                </div>

                <div className="field">
                  <label>Water intake (liters)</label>
                  <input
                    type="number"
                    value={nutritionForm.water_intake}
                    onChange={(e) =>
                      setNutritionForm({ ...nutritionForm, water_intake: e.target.value })
                    }
                    placeholder="e.g. 2.5"
                  />
                  {nutritionErrors.water_intake && (
                    <small className="error">{nutritionErrors.water_intake}</small>
                  )}
                </div>
              </div>

              <p className="modal-hint">
                Tip: You can go back to edit your profile if something is incorrect.
              </p>
            </div>


            <div className="modal-footer">
              <button
                className="btn btn-ghost"
                type="button"
                onClick={() => {
                  setShowNutritionModal(false);
                  setEditingPlan(false);
                }}
              >
                Cancel
              </button>
              <button
                className="btn btn-primary"
                type="button"
                onClick={() => {
                  setShowNutritionModal(false);
                  setEditingPlan(false);
                  setShowProfileModal(true);
                }}

              >
                Back to profile
              </button>
              <button
                className="btn btn-primary"
                type="button"
                onClick={handleGeneratePlan}
                disabled={generating}
              >
                {generating ? "Generating..." : editingPlan ? "Regenerate plan" : "Generate plan"}
              </button>



            </div>
          </div>
        </div>
      )}
    </section>
  );
}

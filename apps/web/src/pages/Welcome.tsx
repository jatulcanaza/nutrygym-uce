import hero from "../assets/hero.jpg";

export default function Welcome() {
  return (
    <section className="hero">
      <div className="hero-text">
        <h1>Bienvenido a NutryGym</h1>
        <p>
          Mejora tu salud, tu nutrición y tu rendimiento con planes personalizados.
        </p>
      </div>

      <div className="hero-img">
        <img src={hero} alt="NutryGym" />
      </div>
    </section>
  );
}

---
title: "Test — Artículo de Prueba Saneamientos"
slug: test-saneamientos-draft
lang: es
excerpt: "Artículo de prueba con banner CTA entre secciones, imagen de portada e índice de contenidos."
---

![Operario de Saneamientos Mungia realizando inspección con cámara robotizada](images/PENDIENTE.jpg)

<nav style="background:#f8f9fa;border-left:4px solid #1a56db;padding:18px 24px;border-radius:0 8px 8px 0;margin-bottom:32px;font-size:15px;line-height:1.8">
<strong style="display:block;margin-bottom:8px;font-size:16px;color:#1a1a2e">Índice de contenidos</strong>
<a href="#que-es-este-test" style="color:#1a56db;text-decoration:none;display:block">1. Qué es este test</a>
<a href="#que-se-ha-probado" style="color:#1a56db;text-decoration:none;display:block">2. Qué se ha probado</a>
<a href="#resultado" style="color:#1a56db;text-decoration:none;display:block">3. Resultado</a>
</nav>

<h2 id="que-es-este-test">Qué es este test</h2>

Este es un **borrador de prueba** generado desde el repositorio local para validar el pipeline completo de publicación. Si ves esto en el panel de WordPress, la conexión funciona correctamente.

En este test comprobamos tres elementos nuevos: el **banner CTA** entre secciones, la **tabla de contenidos** con enlaces funcionales al principio, y el campo de **imagen de portada** en el frontmatter.

<!-- BANNER CTA — Insertar entre secciones del artículo -->
<div style="background:#1a1a2e;border-radius:10px;padding:28px 32px;margin:36px 0;display:flex;align-items:center;gap:24px;flex-wrap:wrap">
  <div style="flex:1;min-width:220px">
    <div style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.07em;color:rgba(255,255,255,.4);margin-bottom:6px">Urgencias 24h · Bizkaia</div>
    <div style="font-size:18px;font-weight:700;color:#fff;line-height:1.3;margin-bottom:6px">¿Problemas con tus tuberías?</div>
    <div style="font-size:13px;color:rgba(255,255,255,.55);line-height:1.5">Más de 30 años de experiencia, maquinaria propia y atención el mismo día.</div>
  </div>
  <div style="display:flex;gap:10px;flex-wrap:wrap">
    <a href="tel:+34944460209" style="display:inline-block;padding:11px 22px;background:#1a56db;color:#fff;border-radius:8px;font-size:14px;font-weight:600;text-decoration:none">Llamar al 944 46 02 09</a>
    <a href="mailto:mungia@saneamientosmungia.com" style="display:inline-block;padding:11px 22px;background:rgba(255,255,255,.08);color:rgba(255,255,255,.8);border-radius:8px;font-size:14px;font-weight:500;text-decoration:none">Enviar email</a>
  </div>
</div>

<h2 id="que-se-ha-probado">Qué se ha probado</h2>

El flujo completo incluye:

- **Frontmatter YAML** con title, slug, excerpt y featured_image
- **Índice de contenidos** con enlaces anchor a cada H2
- **H2 con id HTML** para que los enlaces del índice funcionen
- **Banner CTA inline** entre secciones, sin JavaScript ni position:fixed
- **Autenticación cookie** contra WordPress

<h2 id="resultado">Resultado</h2>

Si estás leyendo esto desde la web y el banner azul oscuro aparece entre las secciones, todo funciona. Este post se puede borrar una vez verificado.

<!-- BANNER CTA — Se puede repetir antes del cierre -->
<div style="background:#1a1a2e;border-radius:10px;padding:28px 32px;margin:36px 0;display:flex;align-items:center;gap:24px;flex-wrap:wrap">
  <div style="flex:1;min-width:220px">
    <div style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.07em;color:rgba(255,255,255,.4);margin-bottom:6px">Urgencias 24h · Bizkaia</div>
    <div style="font-size:18px;font-weight:700;color:#fff;line-height:1.3;margin-bottom:6px">¿Problemas con tus tuberías?</div>
    <div style="font-size:13px;color:rgba(255,255,255,.55);line-height:1.5">Más de 30 años de experiencia, maquinaria propia y atención el mismo día.</div>
  </div>
  <div style="display:flex;gap:10px;flex-wrap:wrap">
    <a href="tel:+34944460209" style="display:inline-block;padding:11px 22px;background:#1a56db;color:#fff;border-radius:8px;font-size:14px;font-weight:600;text-decoration:none">Llamar al 944 46 02 09</a>
    <a href="mailto:mungia@saneamientosmungia.com" style="display:inline-block;padding:11px 22px;background:rgba(255,255,255,.08);color:rgba(255,255,255,.8);border-radius:8px;font-size:14px;font-weight:500;text-decoration:none">Enviar email</a>
  </div>
</div>

# Documentación de la Ontología `mascotas.rdf`

## 1. Información General

| Campo | Valor |
|-------|-------|
| **IRI Base** | `http://www.semanticweb.org/mascotas` |
| **Formato** | RDF/XML (Protégé) |
| **Clases** | 9 |
| **Propiedades Objeto** | 6 |
| **Propiedades Dato** | ~13 |
| **Triples** | 2,370 |

---

## 2. Clases (Classes)

| Clase | Descripción |
|-------|-------------|
| `#Mascota` | Animal doméstico (perro, gato, etc.) |
| `#Especie` | Categoría de animal (Gato, Perro) |
| `#Raza` | Raza específica de una especie |
| `#Dueño` | Persona dueña de una mascota |
| `#Alimento` | Comida para mascotas |
| `#Accesorio` | Accesorios (collar, correa, etc.) |
| `#Cuidado` | Tipos de cuidado (baño, vacunas, etc.) |
| `#Gato` | Subclase de Especie |
| `#Perro` | Subclase de Especie |

---

## 3. Propiedades Objeto (Object Properties)

| Propiedad | Dominio | Rango | Descripción |
|-----------|---------|-------|-------------|
| `#tieneRaza` | Mascota | Raza | La raza de la mascota |
| `#perteneceAEspecie` | Raza | Especie | La especie de la raza |
| `#tieneDueño` | Mascota | Dueño | El dueño de la mascota |
| `#consume` | Mascota | Alimento | Alimento que come |
| `#usa` | Mascota | Accesorio | Accesorio que usa |
| `#requiereCuidado` | Mascota | Cuidado | Cuidado requerido |

---

## 4. Propiedades de Datos (Data Properties)

| Propiedad | Dominio | Rango | Descripción |
|-----------|---------|-------|-------------|
| `#nombreMascota` | Mascota | string | Nombre de la mascota |
| `#nombreRaza` | Raza | string | Nombre de la raza |
| `#nombreEspecie` | Especie | string | Nombre de la especie |
| `#nombreDueño` | Dueño | string | Nombre del dueño |
| `#edadMascota` | Mascota | integer | Edad en años |
| `#pesoMascota` | Mascota | float | Peso en kg |
| `#colorMascota` | Mascota | string | Color del pelaje |
| `#sexoMascota` | Mascota | string | Macho/Hembra |
| `#esterilizado` | Mascota | boolean | Si está esterilizado |
| `#requiereBozal` | Mascota | boolean | Si requiere bozal |
| `#tipoPelaje` | Mascota | string | Tipo de pelaje |
| `#temperamento` | Raza | string | Temperamento de la raza |
| `#marcaAlimento` | Alimento | string | Marca del alimento |
| `#tipoAlimento` | Alimento | string | Tipo (seco/húmedo) |
| `#tipoCuidado` | Cuidado | string | Tipo de cuidado |
| `#frecuenciaCuidado` | Cuidado | string | Frecuencia |

---

## 5. Individuos (Instancias)

| Tipo | Cantidad | Ejemplos |
|------|----------|----------|
| **Mascotas** | 110 | Mascota1 - Mascota110 |
| **Razas** | 30 | Raza1 (Labrador), Raza12 (Siamés), etc. |
| **Especies** | 2 | Especie1 (Gato), Especie2 (Perro) |
| **Dueños** | 60 | Dueño1 - Dueño60 |
| **Alimentos** | 20 | Alimento1 - Alimento20 |
| **Accesorios** | 20 | Accesorio1 - Accesorio20 |
| **Cuidados** | 15 | Cuidado1 - Cuidado15 |

---

## 6. Razas por Especie

### Razas de Perro (pertenece a Especie2)
- Raza1: Labrador Retriever
- Raza2: Bulldog Francés
- Raza3: Pastor Alemán
- Raza4: Golden Retriever
- Raza5: Poodle
- Raza6: Chihuahua
- Raza7: Beagle
- Raza8: Rottweiler
- Raza9: Yorkshire Terrier
- Raza10: Boxer
- Raza21: Doberman
- Raza22: Husky Siberiano
- Raza23: Shih Tzu
- Raza25: Border Collie

### Razas de Gato (pertenece a Especie1)
- Raza11: Persa
- Raza12: Siamés
- Raza13: Maine Coon
- Raza14: Bengala
- Raza15: Ragdoll
- Raza16: British Shorthair
- Raza17: Esfinge
- Raza18: Azul Ruso
- Raza19: Abisinio
- Raza20: Scottish Fold

---

## 7. Consultas SPARQL Útiles

### Buscar mascotas por especie (ej. Perro o Gato)
```sparql
PREFIX : <http://www.semanticweb.org/mascotas#>
SELECT ?nombreMascota ?nombreRaza ?nombreEspecie
WHERE {
  ?mascota a :Mascota .
  ?mascota :nombreMascota ?nombreMascota .
  ?mascota :tieneRaza ?raza .
  ?raza :nombreRaza ?nombreRaza .
  ?raza :perteneceAEspecie ?especie .
  ?especie :nombreEspecie ?nombreEspecie .
  FILTER(?nombreEspecie = "Perro" || ?nombreEspecie = "Gato")
}
```

### Buscar todas las mascotas con su dueña
```sparql
PREFIX : <http://www.semanticweb.org/mascotas#>
SELECT ?mascota ?nombreMascota ?nombreDueño
WHERE {
  ?mascota :nombreMascota ?nombreMascota .
  ?mascota :tieneDueño ?dueño .
  ?dueño :nombreDueño ?nombreDueño .
}
```

### Buscar mascotas por raza
```sparql
PREFIX : <http://www.semanticweb.org/mascotas#>
SELECT ?nombreMascota ?nombreRaza
WHERE {
  ?mascota :nombreMascota ?nombreMascota .
  ?mascota :tieneRaza ?raza .
  ?raza :nombreRaza ?nombreRaza .
  FILTER(?nombreRaza = "Labrador Retriever")
}
```

---

## 8. Esquema de Relaciones

```
Especie (2)
  ├── Especie1 (Gato)
  └── Especie2 (Perro)

Raza (30) ──perteneceAEspecie──> Especie
  ├── Raza1-Raza10, Raza21-Raza25 ──> Especie2 (Perro)
  └── Raza11-Raza20, Raza26-Raza30 ──> Especie1 (Gato)

Mascota (110) ──tieneRaza──> Raza
              ──tieneDueño──> Dueño
              ──consume──> Alimento
              ──usa──> Accesorio
              ──requiereCuidado──> Cuidado
```

---

## 9. Archivo actual

| Archivo | Formato | Descripción |
|---------|---------|-------------|
| `mascotas.rdf` | RDF/XML | Versión compatible con rdflib |

**Nota:** Para usar con Python/rdflib, usar `mascotas.rdf`.
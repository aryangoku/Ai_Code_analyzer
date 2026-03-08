import { useRef, useMemo } from "react"
import { Canvas, useFrame } from "@react-three/fiber"
import { Float } from "@react-three/drei"

function ParticleField() {
  const count = 200
  const positions = useMemo(() => {
    const pos = new Float32Array(count * 3)
    for (let i = 0; i < count; i++) {
      pos[i * 3] = (Math.random() - 0.5) * 20
      pos[i * 3 + 1] = (Math.random() - 0.5) * 20
      pos[i * 3 + 2] = (Math.random() - 0.5) * 12
    }
    return pos
  }, [])
  const ref = useRef()
  useFrame((state) => {
    if (ref.current) ref.current.rotation.y = state.clock.elapsedTime * 0.02
  })
  return (
    <points ref={ref} position={[0, 0, -4]}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={count}
          array={positions}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial size={0.08} color="#818cf8" transparent opacity={0.6} sizeAttenuation />
    </points>
  )
}

function CentralOrb() {
  const ref = useRef()
  useFrame((state) => {
    if (ref.current) ref.current.rotation.y = state.clock.elapsedTime * 0.15
  })
  return (
    <Float speed={1.5} rotationIntensity={0.2} floatIntensity={0.5}>
      <mesh ref={ref} scale={1.2}>
        <icosahedronGeometry args={[1.2, 1]} />
        <meshStandardMaterial
          color="#6366f1"
          emissive="#4338ca"
          emissiveIntensity={0.4}
          metalness={0.6}
          roughness={0.3}
          wireframe={false}
        />
      </mesh>
    </Float>
  )
}

export default function LandingScene() {
  return (
    <div className="absolute inset-0 z-0 overflow-hidden">
      <Canvas
        camera={{ position: [0, 0, 6], fov: 50 }}
        dpr={[1, 1.5]}
        gl={{ alpha: true, antialias: true }}
      >
        <color attach="background" args={["#020617"]} />
        <ambientLight intensity={0.4} />
        <pointLight position={[10, 10, 10]} intensity={1} color="#818cf8" />
        <pointLight position={[-10, -5, 5]} intensity={0.5} color="#a78bfa" />
        <ParticleField />
        <CentralOrb />
      </Canvas>
    </div>
  )
}

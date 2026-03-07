import { Canvas } from "@react-three/fiber"

export default function Background(){

return(

<Canvas>

<mesh rotation={[10,10,0]}>
<torusKnotGeometry args={[3,1,100,16]}/>
<meshStandardMaterial color="purple"/>
</mesh>

</Canvas>

)

}
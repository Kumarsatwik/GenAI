
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { personas, type Persona } from "@/data/personas";

interface PersonaSelectorProps {
  selectedPersona: Persona;
  onSelectPersona: (persona: Persona) => void;
}

export const PersonaSelector = ({
  selectedPersona,
  onSelectPersona,
}: PersonaSelectorProps) => {
  return (
    <div className="p-4 border-b">
      <Select
        value={selectedPersona.id}
        onValueChange={(value) => {
          const persona = personas.find((p) => p.id === value);
          if (persona) onSelectPersona(persona);
        }}
      >
        <SelectTrigger className="w-[200px]">
          <SelectValue>
            <div className="flex items-center gap-2">
             
              <span>{selectedPersona.name}</span>
            </div>
          </SelectValue>
        </SelectTrigger>
        <SelectContent>
          {personas.map((persona) => (
            <SelectItem key={persona.id} value={persona.id}>
              <div className="flex items-center gap-2">
                <span>{persona.name}</span>
              </div>
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
};

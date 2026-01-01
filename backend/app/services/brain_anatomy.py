"""
Brain Anatomy Mapping Service

Maps 2D coordinates on brain MRI to anatomical regions.
"""

from typing import Tuple, Dict


class BrainAnatomyMapper:
    """Maps coordinates to brain regions"""
    
    def identify_region(self, rel_x: float, rel_y: float) -> Dict[str, str]:
        """
        Identify brain region from relative coordinates (0-1 range)
        
        Args:
            rel_x: Horizontal position (0=left, 1=right)
            rel_y: Vertical position (0=top, 1=bottom)
            
        Returns:
            Dictionary with region name and description
        """
        
        # Vertical zones
        top_third = rel_y < 0.33
        middle_third = 0.33 <= rel_y < 0.67
        bottom_third = rel_y >= 0.67
        
        # Horizontal zones
        left_third = rel_x < 0.33
        center_third = 0.33 <= rel_x < 0.67
        right_third = rel_x >= 0.67
        
        # Region identification logic
        if top_third:
            if left_third or right_third:
                return {
                    "name": "Frontal Lobe",
                    "function": "Controls motor function, problem solving, spontaneity, memory, language, initiation, judgement, impulse control, and social behavior"
                }
            else:
                return {
                    "name": "Central/Parietal Region",
                    "function": "Processes sensory information, spatial awareness, and coordinates movement"
                }
        
        elif middle_third:
            if left_third or right_third:
                return {
                    "name": "Temporal Lobe",
                    "function": "Processes auditory information, memory formation, speech, and emotional responses"
                }
            else:
                return {
                    "name": "Deep Brain Structures",
                    "function": "Includes thalamus, basal ganglia - controls movement, emotions, and relays sensory information"
                }
        
        else:  # bottom_third
            if center_third:
                return {
                    "name": "Brainstem",
                    "function": "Controls vital functions like breathing, heart rate, blood pressure, and consciousness"
                }
            elif bottom_third and (left_third or right_third):
                return {
                    "name": "Cerebellum",
                    "function": "Coordinates voluntary movements, balance, posture, and motor learning"
                }
            else:
                return {
                    "name": "Occipital Lobe",
                    "function": "Primary visual processing center, interprets visual information from the eyes"
                }
        
        # Fallback
        return {
            "name": "Brain Tissue",
            "function": "General brain tissue region"
        }


# Global instance
brain_mapper = BrainAnatomyMapper()

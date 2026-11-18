"""
Skin Weight Validator & Normalizer
Enforces cinematic and game-engine rigging standards:
- Maximum 4 bone influences per vertex (prevents GPU skinning bottlenecks)
- Normalized weights strictly summing to 1.0000
- No orphaned or unweighted vertices
"""

from typing import Dict, List, Tuple, Any

class SkinWeightValidator:
    """Validates and fixes vertex skinning weights for high-fidelity 3D meshes."""

    @classmethod
    def validate_and_normalize(
        cls,
        vertex_weights: Dict[int, List[Tuple[str, float]]],
        max_influences: int = 4
    ) -> Tuple[Dict[int, List[Tuple[str, float]]], Dict[str, Any]]:
        """
        Normalizes weights to 1.0, limits to top max_influences, and reports statistics.
        """
        cleaned_weights = {}
        orphaned_verts = []
        truncated_count = 0

        for v_idx, influences in vertex_weights.items():
            if not influences:
                orphaned_verts.append(v_idx)
                continue

            # Sort by weight descending
            sorted_inf = sorted(influences, key=lambda x: x[1], reverse=True)

            if len(sorted_inf) > max_influences:
                sorted_inf = sorted_inf[:max_influences]
                truncated_count += 1

            total_w = sum(w for _, w in sorted_inf)
            if total_w > 0.0:
                normalized = [(b, w / total_w) for b, w in sorted_inf]
            else:
                normalized = sorted_inf

            cleaned_weights[v_idx] = normalized

        report = {
            "total_vertices": len(vertex_weights),
            "orphaned_vertices_count": len(orphaned_verts),
            "truncated_influences_count": truncated_count,
            "max_influences_enforced": max_influences,
            "is_valid": len(orphaned_verts) == 0
        }
        return cleaned_weights, report

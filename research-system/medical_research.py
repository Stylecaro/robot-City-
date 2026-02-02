"""
Sistema de Investigación Médica Real - Ciudad Robot Metaverso
Simulaciones de laboratorios médicos, experimentos y desarrollo de tratamientos
"""

from enum import Enum
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import uuid
import random

class MedicalResearchType(Enum):
    """Tipos de investigación médica"""
    DRUG_DEVELOPMENT = "drug_development"
    VACCINE_RESEARCH = "vaccine_research"
    GENE_THERAPY = "gene_therapy"
    CANCER_TREATMENT = "cancer_treatment"
    NEURAL_SCIENCE = "neural_science"
    TISSUE_ENGINEERING = "tissue_engineering"
    REGENERATIVE_MEDICINE = "regenerative_medicine"
    DIAGNOSTIC_TOOLS = "diagnostic_tools"
    BIOTECHNOLOGY = "biotechnology"
    IMMUNOLOGY = "immunology"

class ExperimentType(Enum):
    """Tipos de experimentos simulados"""
    CELL_CULTURE = "cell_culture"
    MOLECULAR_ANALYSIS = "molecular_analysis"
    PROTEIN_SYNTHESIS = "protein_synthesis"
    DNA_SEQUENCING = "dna_sequencing"
    DRUG_SCREENING = "drug_screening"
    CLINICAL_TRIAL = "clinical_trial"
    PATHOGEN_STUDY = "pathogen_study"
    TISSUE_SAMPLE = "tissue_sample"

class ResearchPhase(Enum):
    """Fases de investigación"""
    HYPOTHESIS = 1
    DESIGN = 2
    EXPERIMENTATION = 3
    ANALYSIS = 4
    VALIDATION = 5
    PUBLICATION = 6

class MedicalExperiment:
    """Experimento médico simulado"""
    def __init__(self, experiment_type: ExperimentType, complexity: int = 3):
        self.experiment_id = str(uuid.uuid4())
        self.experiment_type = experiment_type
        self.complexity = complexity  # 1-5
        self.duration_hours = complexity * 4
        self.success_rate = max(30, 90 - (complexity * 10))
        self.cost = complexity * 500
        self.reward_multiplier = complexity * 1.5
        self.equipment_required = self._get_equipment()
        self.parameters = self._generate_parameters()
        
    def _get_equipment(self) -> List[str]:
        """Equipamiento necesario"""
        equipment_sets = {
            ExperimentType.CELL_CULTURE: ["Incubator", "Microscope", "Petri Dishes", "Growth Medium"],
            ExperimentType.MOLECULAR_ANALYSIS: ["Spectrophotometer", "Centrifuge", "PCR Machine"],
            ExperimentType.PROTEIN_SYNTHESIS: ["Bioreactor", "Chromatography System", "Lyophilizer"],
            ExperimentType.DNA_SEQUENCING: ["Sequencer", "Thermal Cycler", "Gel Electrophoresis"],
            ExperimentType.DRUG_SCREENING: ["High-Throughput Screener", "Plate Reader", "Liquid Handler"],
            ExperimentType.CLINICAL_TRIAL: ["Patient Monitoring", "Data Collection System", "Safety Equipment"],
            ExperimentType.PATHOGEN_STUDY: ["BSL-3 Lab", "Containment System", "Decontamination Unit"],
            ExperimentType.TISSUE_SAMPLE: ["Biopsy Tools", "Cryopreservation", "Histology Equipment"]
        }
        return equipment_sets.get(self.experiment_type, ["Basic Lab Equipment"])
    
    def _generate_parameters(self) -> Dict:
        """Genera parámetros del experimento"""
        return {
            "temperature": random.randint(20, 37),
            "ph_level": round(random.uniform(6.5, 7.5), 2),
            "concentration": random.randint(1, 100),
            "duration_minutes": random.randint(30, 240),
            "sample_size": random.randint(10, 1000)
        }
    
    def simulate_execution(self, researcher_skill: int) -> Dict:
        """Simula la ejecución del experimento"""
        # Ajustar tasa de éxito basada en habilidad del investigador
        adjusted_success_rate = min(95, self.success_rate + researcher_skill)
        
        success = random.randint(1, 100) <= adjusted_success_rate
        
        result = {
            "experiment_id": self.experiment_id,
            "success": success,
            "completion_time": datetime.now().isoformat(),
            "data_quality": random.randint(60, 100) if success else random.randint(20, 60),
            "breakthrough": False,
            "findings": []
        }
        
        if success:
            # Posibilidad de descubrimiento importante
            if random.randint(1, 100) <= 10:  # 10% chance
                result["breakthrough"] = True
                result["data_quality"] = random.randint(90, 100)
            
            result["findings"] = self._generate_findings()
        
        return result
    
    def _generate_findings(self) -> List[str]:
        """Genera hallazgos del experimento"""
        findings = [
            "Increased cellular activity observed",
            "Positive molecular markers detected",
            "Successful protein binding confirmed",
            "Minimal toxicity in test samples",
            "Improved therapeutic efficacy shown",
            "Novel interaction pathway identified",
            "Enhanced bioavailability measured",
            "Stable compound formation achieved"
        ]
        return random.sample(findings, k=random.randint(2, 4))
    
    def to_dict(self) -> Dict:
        return {
            "experiment_id": self.experiment_id,
            "type": self.experiment_type.value,
            "complexity": self.complexity,
            "duration_hours": self.duration_hours,
            "success_rate": self.success_rate,
            "cost": self.cost,
            "equipment": self.equipment_required,
            "parameters": self.parameters
        }

class MedicalResearchProject:
    """Proyecto de investigación médica"""
    def __init__(self, research_type: MedicalResearchType, title: str):
        self.project_id = str(uuid.uuid4())
        self.research_type = research_type
        self.title = title
        self.description = ""
        self.phase = ResearchPhase.HYPOTHESIS
        self.progress_percent = 0.0
        self.budget = 0
        self.budget_spent = 0
        self.team_size = 1
        self.experiments_completed = 0
        self.publications = 0
        self.start_date = datetime.now()
        self.estimated_completion = self.start_date + timedelta(days=180)
        self.findings: List[Dict] = []
        self.impact_score = 0  # 0-100
        
    def advance_phase(self) -> bool:
        """Avanza a la siguiente fase"""
        if self.progress_percent >= 100:
            current_phase_value = self.phase.value
            if current_phase_value < 6:
                self.phase = ResearchPhase(current_phase_value + 1)
                self.progress_percent = 0.0
                return True
        return False
    
    def add_experiment_result(self, experiment_result: Dict):
        """Añade resultado de experimento"""
        self.experiments_completed += 1
        self.findings.append(experiment_result)
        
        # Incrementar progreso
        progress_gain = 10 if experiment_result["success"] else 5
        if experiment_result.get("breakthrough", False):
            progress_gain = 25
            self.impact_score += 10
        
        self.progress_percent = min(100, self.progress_percent + progress_gain)
        
        # Auto-avanzar fase si es necesario
        self.advance_phase()
    
    def publish_paper(self) -> Dict:
        """Publica un paper científico"""
        if self.experiments_completed < 3:
            return {"error": "Necesitas al menos 3 experimentos completados"}
        
        self.publications += 1
        citations = random.randint(10, 100) * self.impact_score
        impact_factor = round(random.uniform(1.0, 10.0), 2)
        
        return {
            "publication_id": str(uuid.uuid4()),
            "project_id": self.project_id,
            "title": f"{self.title} - Research Findings",
            "citations": citations,
            "impact_factor": impact_factor,
            "date": datetime.now().isoformat()
        }
    
    def to_dict(self) -> Dict:
        return {
            "project_id": self.project_id,
            "research_type": self.research_type.value,
            "title": self.title,
            "description": self.description,
            "phase": self.phase.name,
            "progress_percent": round(self.progress_percent, 2),
            "budget": self.budget,
            "budget_spent": self.budget_spent,
            "team_size": self.team_size,
            "experiments_completed": self.experiments_completed,
            "publications": self.publications,
            "start_date": self.start_date.isoformat(),
            "estimated_completion": self.estimated_completion.isoformat(),
            "impact_score": self.impact_score,
            "findings_count": len(self.findings)
        }

class MedicalLaboratory:
    """Laboratorio médico"""
    def __init__(self, name: str, specialization: MedicalResearchType):
        self.lab_id = str(uuid.uuid4())
        self.name = name
        self.specialization = specialization
        self.level = 1
        self.reputation = 0
        self.equipment_quality = 50  # 0-100
        self.safety_rating = 80  # 0-100
        self.active_projects: List[MedicalResearchProject] = []
        self.completed_projects: List[str] = []
        self.researchers: List[Dict] = []
        self.funding = 10000
        
    def hire_researcher(self, researcher_name: str, skill_level: int) -> Dict:
        """Contrata investigador"""
        researcher = {
            "researcher_id": str(uuid.uuid4()),
            "name": researcher_name,
            "skill_level": skill_level,
            "specialization": self.specialization.value,
            "experiments_conducted": 0,
            "success_rate": 50 + skill_level * 5
        }
        self.researchers.append(researcher)
        return researcher
    
    def upgrade_equipment(self, amount: int) -> Dict:
        """Mejora equipamiento"""
        cost = amount * 100
        if self.funding < cost:
            return {"error": "Fondos insuficientes"}
        
        self.funding -= cost
        old_quality = self.equipment_quality
        self.equipment_quality = min(100, self.equipment_quality + amount)
        
        return {
            "success": True,
            "old_quality": old_quality,
            "new_quality": self.equipment_quality,
            "cost": cost
        }
    
    def start_project(self, project: MedicalResearchProject) -> bool:
        """Inicia proyecto de investigación"""
        if len(self.active_projects) >= 5:
            return False
        
        self.active_projects.append(project)
        return True
    
    def to_dict(self) -> Dict:
        return {
            "lab_id": self.lab_id,
            "name": self.name,
            "specialization": self.specialization.value,
            "level": self.level,
            "reputation": self.reputation,
            "equipment_quality": self.equipment_quality,
            "safety_rating": self.safety_rating,
            "active_projects": len(self.active_projects),
            "completed_projects": len(self.completed_projects),
            "researchers": len(self.researchers),
            "funding": self.funding
        }

class MedicalResearchManager:
    """Gestor central de investigación médica"""
    def __init__(self):
        self.laboratories: Dict[str, MedicalLaboratory] = {}
        self.projects: Dict[str, MedicalResearchProject] = {}
        self.experiments: Dict[str, MedicalExperiment] = {}
        self._initialize_templates()
    
    def _initialize_templates(self):
        """Crea plantillas de proyectos"""
        self.project_templates = {
            MedicalResearchType.DRUG_DEVELOPMENT: [
                "Novel Antibiotic Discovery",
                "Cancer Drug Synthesis",
                "Antiviral Compound Development"
            ],
            MedicalResearchType.VACCINE_RESEARCH: [
                "mRNA Vaccine Platform",
                "Universal Flu Vaccine",
                "HIV Vaccine Development"
            ],
            MedicalResearchType.GENE_THERAPY: [
                "CRISPR Gene Editing",
                "Genetic Disease Treatment",
                "Gene Delivery Systems"
            ],
            MedicalResearchType.CANCER_TREATMENT: [
                "Immunotherapy Research",
                "Targeted Cancer Therapy",
                "Early Detection Methods"
            ],
            MedicalResearchType.NEURAL_SCIENCE: [
                "Alzheimer's Treatment",
                "Brain-Computer Interface",
                "Neuroprotective Compounds"
            ]
        }
    
    def create_laboratory(self, name: str, specialization: MedicalResearchType) -> MedicalLaboratory:
        """Crea laboratorio"""
        lab = MedicalLaboratory(name, specialization)
        self.laboratories[lab.lab_id] = lab
        return lab
    
    def create_project(self, lab_id: str, research_type: MedicalResearchType, title: str) -> Dict:
        """Crea proyecto de investigación"""
        lab = self.laboratories.get(lab_id)
        if not lab:
            return {"error": "Laboratorio no encontrado"}
        
        project = MedicalResearchProject(research_type, title)
        project.budget = 50000
        
        if lab.start_project(project):
            self.projects[project.project_id] = project
            return {"success": True, "project": project.to_dict()}
        else:
            return {"error": "Laboratorio tiene demasiados proyectos activos"}
    
    def create_experiment(self, experiment_type: ExperimentType, complexity: int) -> MedicalExperiment:
        """Crea experimento"""
        experiment = MedicalExperiment(experiment_type, complexity)
        self.experiments[experiment.experiment_id] = experiment
        return experiment
    
    def run_experiment(self, experiment_id: str, project_id: str, researcher_skill: int = 5) -> Dict:
        """Ejecuta experimento"""
        experiment = self.experiments.get(experiment_id)
        project = self.projects.get(project_id)
        
        if not experiment or not project:
            return {"error": "Experimento o proyecto no encontrado"}
        
        # Simular ejecución
        result = experiment.simulate_execution(researcher_skill)
        
        # Añadir a proyecto
        project.add_experiment_result(result)
        project.budget_spent += experiment.cost
        
        return result
    
    def get_research_stats(self) -> Dict:
        """Estadísticas globales"""
        total_experiments = sum(p.experiments_completed for p in self.projects.values())
        total_publications = sum(p.publications for p in self.projects.values())
        avg_impact = sum(p.impact_score for p in self.projects.values()) / max(1, len(self.projects))
        
        return {
            "total_laboratories": len(self.laboratories),
            "active_projects": len([p for p in self.projects.values() if p.progress_percent < 100]),
            "completed_projects": len([p for p in self.projects.values() if p.progress_percent >= 100]),
            "total_experiments": total_experiments,
            "total_publications": total_publications,
            "average_impact_score": round(avg_impact, 2)
        }

# Instancia global
medical_research_manager = MedicalResearchManager()

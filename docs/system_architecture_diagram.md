# System Architecture & Data Flow

This diagram strictly details the technical components and the flow of data through the system, from the client interface down to the deterministic processing and generative AI layers.

```mermaid
flowchart TD
    %% Define external actors and boundaries
    User((End User))
    
    subgraph Frontend [Frontend Tier]
        UI[Streamlit Web App]
    end

    subgraph API_Layer [API & Request Handling]
        AppLogic[Main Application Logic]
        Validation[Pydantic UserPreferences Schema]
    end

    subgraph Processing_Layer [Deterministic Data Engine]
        FilterEngine[Pandas Filter Engine]
        Parquet[(Clean Catalog Data .parquet)]
    end

    subgraph AI_Layer [Generative AI Orchestration]
        PromptBuilder[Prompt Builder]
        GroqClient[Groq LLM Client]
        DataMerger[Response Merger]
    end

    subgraph External [External APIs]
        GroqAPI((Groq Cloud API))
    end

    %% Data Flow Steps
    User -->|1. Enters Search Criteria| UI
    UI -->|2. Raw Input Dictionary| AppLogic
    AppLogic -->|3. Validate & Parse| Validation
    Validation -.->|Validated UserPreferences| AppLogic
    
    AppLogic -->|4. Search Constraints| FilterEngine
    FilterEngine <-->|5. In-Memory Read & Filter| Parquet
    FilterEngine -->|6. Tabular Shortlist| AppLogic
    
    AppLogic -->|7. Shortlist + User Context| PromptBuilder
    PromptBuilder -->|8. System & User Prompt| GroqClient
    GroqClient <-->|9. Network Req/Res| GroqAPI
    GroqClient -->|10. Extracted AI Explanations| DataMerger
    
    DataMerger -->|11. Enhanced Result Set| AppLogic
    AppLogic -->|12. Render Responsive Cards| UI
    UI -->|13. Visual Results| User

    %% Styling for visual distinction
    classDef frontend fill:#1e293b,stroke:#3b82f6,stroke-width:2px,color:#fff
    classDef api fill:#0f172a,stroke:#10b981,stroke-width:2px,color:#fff
    classDef proc fill:#0f172a,stroke:#f59e0b,stroke-width:2px,color:#fff
    classDef ai fill:#0f172a,stroke:#a855f7,stroke-width:2px,color:#fff
    classDef db fill:#334155,stroke:#94a3b8,stroke-width:2px,color:#fff
    classDef actor fill:#475569,stroke:#94a3b8,stroke-width:2px,color:#fff
    
    class UI frontend;
    class AppLogic,Validation api;
    class FilterEngine proc;
    class Parquet db;
    class PromptBuilder,GroqClient,DataMerger ai;
    class GroqAPI,User actor;
```

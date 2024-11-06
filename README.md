# SceneCrafter: Automating Scene Setup and Recommending Next Step in Godot

## Project Description

**SceneCrafter** is an AI-powered plugin designed to enhance the Godot Engine's scene creation process. By leveraging natural language input and real-time contextual recommendations, SceneCrafter aims to streamline the workflow for game developers, especially those who work in smaller teams or are just starting with Godot. 

SceneCrafter enables developers to:
- Describe scenes in natural language, allowing the tool to automatically generate the required nodes, configure properties, and attach scripts.
- Receive real-time, context-aware suggestions while building scenes, such as prompts for missing scripts or suggestions for configuring signals based on the user's actions in the Godot editor.

This plugin integrates seamlessly into the Godot Editor, providing a user-friendly interface and intelligent guidance to simplify and accelerate the game development process.

## Motivation

Game developers often balance creative work with technical tasks, and scene creation in Godot can become tedious due to its manual nature. Existing code suggestion tools like GitHub Copilot lack support for visual scene setup and real-time scene guidance. SceneCrafter addresses this gap by providing an intelligent assistant that reduces repetitive tasks and offers context-based recommendations, thus boosting productivity and easing the learning curve for new developers.

Godot's open-source nature, zero licensing fees, and lightweight architecture make it an affordable and accessible solution for developers. Unlike other engines with restrictive fees, Godot’s flexibility supports developers of free or small-scale commercial games, making SceneCrafter an invaluable addition to this ecosystem.

## Problem Description (User Story)

Developers often encounter repetitive and error-prone tasks when creating scenes in Godot. For example, a developer may spend hours manually adding nodes, configuring properties, and attaching scripts, which can hinder productivity. The developer wishes for an intelligent assistant that interprets natural language descriptions to generate nodes and offers real-time, context-aware suggestions. For instance:
- If a node is added without a script, the tool could suggest attaching one or provide a pre-written script based on the node's properties.
- If signals are needed between nodes, the tool could suggest appropriate connections.

## Proposed Features

1. **Input Parsing and Mapping**: The plugin transforms plain text input into actionable commands, identifying actions, node types, and script details for scene setup.

2. **Prompt-Based Scene Creation**: Automatically generates required nodes, attaching relevant scripts and setting up the scene's initial configuration based on user descriptions.

3. **Monitoring User Actions**: Observes user actions, such as adding or modifying nodes, to better understand the context and provide accurate suggestions.

4. **Real-Time Suggestions**: Provides contextual guidance, such as:
   - Attaching missing scripts to nodes.
   - Configuring animations and optimizing the scene structure.
   - Suggesting signal setups between nodes for enhanced interactivity.

5. **Automated Code Generation**: Assists in script creation by suggesting code snippets relevant to the scene context.

6. **Feedback Mechanism**: Collects data on user interactions to refine suggestions over time, creating a personalized and adaptive assistant.

7. **Non-Intrusive Editor Integration**: Developed as a plugin without modifying Godot’s source code, ensuring easy installation and compatibility with the editor.

## Languages and Tools

- **Languages**:
  - **GDScript**: Used for Godot-specific scripting and scene manipulation.
  - **Python**: For integrating Natural Language Processing (NLP) capabilities.
  - **JSON**: For data handling and scene generation.

- **Tools and APIs**:
  - **Godot Editor Plugin**: Embeds the assistant within the Godot editor.
  - **Godot SceneTree**: Creates nodes and configures scenes programmatically.
  - **EditorInspectorPlugin**: Monitors user actions for context-aware suggestions.
  - **NLP Tools**: Uses Hugging Face Transformers to parse natural language input.
  - **UI Development**: Utilizes Godot's `Control` nodes to build the prompt and suggestion interface.

## Getting Started

### Prerequisites

- **Godot Engine**: Install the latest version of Godot.
- **Python**: Required for NLP processing.
- **Hugging Face Transformers**: Install with `pip install transformers`.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/SceneCrafter.git
   ```
2. Install required Python dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Copy the `SceneCrafter` folder into your Godot project’s `addons` directory.
4. Enable the SceneCrafter plugin in Godot via `Project -> Project Settings -> Plugins`.

### Usage

1. Start the Godot Editor and open the **SceneCrafter** plugin UI.
2. Describe the scene you want to create in natural language, and SceneCrafter will generate nodes and configure properties.
3. Receive real-time suggestions as you modify your scene, such as script attachment prompts and signal configuration advice.

## Project Structure

```plaintext
SceneCrafter/
├── backend/
│   ├── main.py                 # Backend logic for NLP processing
│   ├── functions.py             # Helper functions for processing commands
│   ├── requirements.txt         # Python dependencies
│   └── ...                      # Additional backend scripts
├── scene-crafter/
│   ├── plugin.cfg               # Godot plugin configuration
│   ├── SceneCrafter.gd          # Main plugin script
│   ├── UI/                      # Custom UI elements for SceneCrafter
│   └── ...                      # Additional Godot scripts and scenes
├── README.md                    # Project documentation
└── commands.md                  # Command usage documentation
```

## Contributing

1. Fork the repository and create your branch.
2. Make your changes and test thoroughly.
3. Create a pull request, explaining the changes you made.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
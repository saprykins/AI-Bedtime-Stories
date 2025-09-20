# Story Teller AI Agent 🎭

A goal-oriented AI agent that creates personalized children's stories to help address behavioral problems through gentle, therapeutic storytelling.

## Overview

The Story Teller AI Agent processes descriptions of children's behavioral challenges and creates personalized fairy tales that teach appropriate behavior through engaging storytelling. The agent uses a three-tool pipeline:

1. **Text Analysis Tool** - Analyzes the behavioral problem and extracts key story elements
2. **Story Generation Tool** - Creates a personalized fairy tale with appropriate moral lessons
3. **Text-to-Speech Tool** - Converts the story into an audio file for easy sharing

## Features

- 🧠 **Intelligent Analysis**: Extracts problem types, emotions, and appropriate moral lessons
- 📚 **Personalized Stories**: Creates unique fairy tales with animal characters using AI
- 🎵 **Audio Generation**: Converts stories to high-quality audio files (with text fallback)
- 🎯 **Non-Accusatory**: Uses gentle storytelling to teach lessons without direct criticism
- 🖥️ **Terminal-Based**: Simple command-line interface for easy use
- 🔄 **Fallback Modes**: Works even without Azure credentials using built-in templates
- 🛠️ **Robust Error Handling**: Graceful degradation when services are unavailable

## Prerequisites

- Python 3.8 or higher
- **Optional**: Azure account with access to:
  - Azure OpenAI Service (for AI-powered story generation)
  - Azure Cognitive Services Speech (for audio generation)

**Note**: The agent works without Azure credentials using built-in fallback modes, but Azure services provide much better story quality and audio generation.

## Azure Setup Instructions

### 1. Azure OpenAI Service Setup

1. **Create an Azure OpenAI Resource**:
   - Go to [Azure Portal](https://portal.azure.com)
   - Search for "Azure OpenAI" and create a new resource
   - Choose your subscription, resource group, and region
   - Select a pricing tier (S0 Standard is sufficient for testing)

2. **Deploy a Model**:
   - In your Azure OpenAI resource, go to "Model deployments"
   - Click "Create new deployment"
   - Choose a model (recommended: `gpt-4` or `gpt-35-turbo`)
   - Give it a deployment name (e.g., `gpt-4-deployment`)
   - Note the deployment name for later use

3. **Get Your Credentials**:
   - In your Azure OpenAI resource, go to "Keys and Endpoint"
   - Copy the following values:
     - **API Key** (either Key 1 or Key 2)
     - **Endpoint** (the full URL)
     - **API Version** (usually `2024-02-15-preview`)

### 2. Azure Speech Services Setup

1. **Create a Speech Services Resource**:
   - Go to [Azure Portal](https://portal.azure.com)
   - Search for "Speech Services" and create a new resource
   - Choose your subscription, resource group, and region
   - Select a pricing tier (F0 Free tier is available for testing)

2. **Get Your Speech Credentials**:
   - In your Speech Services resource, go to "Keys and Endpoint"
   - Copy the following values:
     - **Key 1** (or Key 2)
     - **Region** (e.g., `eastus`, `westus2`)

### 3. Environment Variables Setup

Create a `.env` file in the project root with your Azure credentials:

```bash
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_openai_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-12-01-preview
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name_here

# Azure Speech Services Configuration
AZURE_SPEECH_KEY=your_speech_key_here
AZURE_SPEECH_REGION=your_speech_region_here

# Optional: Customize voice and output
AZURE_VOICE_NAME=en-US-AriaNeural
OUTPUT_DIR=./output
```

**Important**: 
- Never commit the `.env` file to version control. It's already included in `.gitignore`.
- If the `.env` file has encoding issues, the script will automatically use fallback credentials.
- The script works without Azure credentials using built-in templates.

## Installation

1. **Clone or download the project**:
   ```bash
   git clone <repository-url>
   cd story-tellers
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (optional):
   - Copy the example `.env` file and fill in your Azure credentials
   - Or set environment variables directly in your shell
   - **The script works without Azure credentials using fallback modes**

## Usage

### Basic Usage

Run the agent with a description of the child's behavioral problem:

```bash
python story_agent.py "My son got into a fight at school because he didn't want to share a toy."
```

### Advanced Usage

```bash
# Specify custom output directory
python story_agent.py "My daughter won't clean her room" --output-dir ./my-stories

# Get help
python story_agent.py --help
```

### Example Prompts

Here are some example behavioral problems you can use:

```bash
# Sharing issues
python story_agent.py "My child refuses to share toys with friends"

# Listening problems
python story_agent.py "My son keeps interrupting when adults are talking"

# Lying
python story_agent.py "My daughter has been telling small lies about homework"

# Aggression
python story_agent.py "My child has been hitting other kids at daycare"

# Following instructions
python story_agent.py "My son won't clean up his toys when asked"
```

## Output

The agent will:

1. **Analyze** the problem and extract key elements
2. **Generate** a personalized fairy tale (300-500 words)
3. **Create** an audio file (WAV format) or text file in the output directory
4. **Display** a confirmation message with the file path

### Example Output (with Azure credentials):
```
🎭 Story Teller AI Agent starting...
📝 Processing: My son got into a fight at school because he didn't want to share a toy.

🔍 Tool 1: Analyzing the problem...
✅ Analysis complete: sharing conflict - sharing and taking turns helps everyone have fun and feel happy

📚 Tool 2: Generating personalized story...
✅ Story generated successfully

🎵 Tool 3: Converting story to audio...
🎤 Synthesizing speech... (this may take a moment)
[32m✅ Audio saved to: ./output/story_1703123456.wav[0m

🎉 Story generated and saved successfully!
[32m📁 Audio file: ./output/story_1703123456.wav[0m

💡 Tip: Play the audio file to share the story with your child!
```

### Example Output (fallback mode):
```
🎭 Story Teller AI Agent starting...
📝 Processing: My son got into a fight at school because he didn't want to share a toy.

🔍 Tool 1: Analyzing the problem...
⚠️  Azure OpenAI not configured. Using fallback analysis.
✅ Analysis complete: sharing conflict - the importance of sharing and friendship

📚 Tool 2: Generating personalized story...
⚠️  Azure OpenAI not configured. Using fallback story generation.
✅ Story generated successfully

🎵 Tool 3: Converting story to audio...
⚠️  Azure Speech Services not available. Text-to-speech will be disabled.
📝 Story saved as text file: ./output/story_1703123456.txt
💡 To enable audio generation, please set up Azure Speech Services credentials.
✅ Audio saved to: ./output/story_1703123456.txt

🎉 Story generated and saved successfully!
📁 Audio file: ./output/story_1703123456.txt

💡 Tip: Play the audio file to share the story with your child!
```

## Project Structure

```
story-tellers/
├── story_agent.py          # Main agent orchestrator
├── tools/
│   ├── __init__.py
│   ├── text_analysis.py    # Tool 1: Problem analysis
│   ├── story_generation.py # Tool 2: Story creation
│   └── text_to_speech.py   # Tool 3: Audio generation
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .env.example           # Environment variables template
└── output/                # Generated audio files (created automatically)
```

## Customization

### Voice Selection

You can customize the voice used for speech synthesis by setting the `AZURE_VOICE_NAME` environment variable:

```bash
# Available child-friendly voices
AZURE_VOICE_NAME=en-US-AriaNeural    # Warm, friendly female (default)
AZURE_VOICE_NAME=en-US-JennyNeural   # Clear, professional female
AZURE_VOICE_NAME=en-US-GuyNeural     # Warm male voice
AZURE_VOICE_NAME=en-US-DavisNeural   # Friendly male voice
```

### Story Length and Style

The stories are automatically optimized for:
- **Length**: 300-500 words (3-5 minute audio)
- **Age**: 4-8 years old
- **Tone**: Warm, magical, and encouraging
- **Structure**: Beginning, challenge, resolution with moral lesson

## Troubleshooting

### Common Issues

1. **"Failed to initialize Azure OpenAI client"**:
   - Check your `AZURE_OPENAI_API_KEY` and `AZURE_OPENAI_ENDPOINT`
   - Ensure your deployment name is correct
   - **Note**: The script will use fallback story generation if Azure OpenAI is unavailable

2. **"Azure Speech Services credentials not found"**:
   - Verify your `AZURE_SPEECH_KEY` and `AZURE_SPEECH_REGION`
   - Make sure your Speech Services resource is active
   - **Note**: The script will save stories as text files if Speech Services is unavailable

3. **"Speech synthesis failed"**:
   - Check your Speech Services quota and billing
   - Verify the voice name is valid
   - On Windows, you may need to install Visual C++ Redistributable for the Azure Speech SDK

4. **Import errors**:
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check your Python version (3.8+ required)
   - Make sure you're using the virtual environment: `venv\Scripts\activate` (Windows)

5. **".env file encoding issues"**:
   - The script automatically handles encoding issues and uses fallback credentials
   - If problems persist, set environment variables directly in your shell

6. **"Azure Speech SDK DLL not found" (Windows)**:
   - This is a known issue with the Azure Speech SDK on some Windows systems
   - The script will automatically fall back to text file output
   - To fix: Install Microsoft Visual C++ Redistributable or use a different Python version

### Getting Help

- Check the Azure Portal for service status
- Review the Azure OpenAI and Speech Services documentation
- Ensure your Azure resources are in the same region for optimal performance

## Fallback Modes

The Story Teller AI Agent includes robust fallback modes that allow it to work even without Azure credentials:

### Text Analysis Fallback
- Uses keyword-based analysis to identify problem types
- Extracts emotions and moral lessons from simple text patterns
- Provides appropriate character suggestions based on the problem type

### Story Generation Fallback
- Uses pre-built story templates for common behavioral issues
- Includes specific templates for sharing conflicts, aggression, lying, and listening problems
- Generates age-appropriate stories with proper moral lessons

### Text-to-Speech Fallback
- Saves stories as text files when Azure Speech Services is unavailable
- Files are saved in the `./output` directory with timestamps
- Stories can be read aloud manually or converted using other tools

### Benefits of Fallback Modes
- **Immediate functionality**: Works out of the box without setup
- **No cost**: No Azure service charges when using fallback modes
- **Reliability**: Always produces a story, even with service outages
- **Learning tool**: Great for understanding how the agent works before setting up Azure services

## Cost Considerations

- **Azure OpenAI**: Pay per token usage (very low cost for short stories)
- **Azure Speech Services**: Pay per character converted to speech
- **Estimated cost**: Less than $0.01 per story for typical usage

## License

This project is provided as-is for educational and personal use. Please ensure you comply with Azure's terms of service and usage policies.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the agent's functionality and story quality.

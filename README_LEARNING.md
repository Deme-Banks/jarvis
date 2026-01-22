# JARVIS Self-Learning System

## Overview

JARVIS now includes a comprehensive self-learning system that learns from every interaction, adapts to your preferences, and improves over time.

## Features

### 1. **Persistent Memory**
- Saves all conversations
- Remembers user preferences
- Builds a knowledge base
- Learns patterns from interactions

### 2. **Adaptive Learning**
- Learns your communication style
- Adapts response length and detail level
- Remembers favorite topics
- Learns successful patterns

### 3. **LLM-Powered Learning**
- Uses AI to analyze conversations
- Extracts insights automatically
- Improves responses based on patterns
- Personalizes interactions

### 4. **Feedback Loop**
- Learns from explicit feedback
- Implicit success detection
- Continuous improvement
- Pattern recognition

## Usage

### Basic Usage

```bash
python3 jarvis_learning.py
```

JARVIS will automatically:
- Learn from every conversation
- Remember your preferences
- Improve over time
- Build knowledge base

### Learning Commands

**Check Learning Progress:**
```
"Jarvis, what have you learned?"
"Jarvis, show learning stats"
```

**Reset Learning:**
```
"Jarvis, forget everything"
"Jarvis, reset learning"
```

### How It Learns

1. **From Conversations**
   - Saves every interaction
   - Analyzes patterns
   - Extracts preferences

2. **From Preferences**
   - Response style (brief/detailed)
   - Speech rate preferences
   - Favorite topics
   - Communication style

3. **From Knowledge**
   - Facts you tell it
   - Information from conversations
   - Context from interactions

4. **From Patterns**
   - Successful response patterns
   - Common request types
   - User behavior patterns

## Learning Data Storage

All learning data is stored in `./memory/`:
- `conversations.json` - Conversation history
- `preferences.json` - Learned preferences
- `knowledge.json` - Knowledge base
- `patterns.pkl` - Learned patterns

## Examples

### Learning Preferences

**User:** "Jarvis, give me shorter answers"
**JARVIS:** Learns you prefer brief responses
**Future:** All responses become more concise

**User:** "Jarvis, explain in more detail"
**JARVIS:** Learns you prefer detailed explanations
**Future:** Responses include more context

### Learning Knowledge

**User:** "My favorite programming language is Python"
**JARVIS:** Saves this to knowledge base
**Future:** When discussing programming, mentions Python preference

### Learning Patterns

**User:** "Jarvis, create a keylogger"
**JARVIS:** Creates keylogger, you say "thanks"
**JARVIS:** Learns this pattern was successful
**Future:** Similar requests get similar successful responses

## Integration

### With Cybersecurity Module

```python
from jarvis_learning import JarvisLearning
from cybersecurity.enhanced_integration import EnhancedCybersecurityOrchestrator

jarvis = JarvisLearning()
# Learning works automatically with all modules
```

### With Voice Interface

Learning works seamlessly with voice:
- Learns speech patterns
- Adapts to voice preferences
- Remembers voice commands

## Performance

- **Memory Usage**: ~1MB per 1000 conversations
- **Learning Speed**: Real-time, no delay
- **Storage**: Persistent across sessions
- **Privacy**: All data stored locally

## Privacy & Security

- All learning data stored locally
- No external data transmission
- User can reset at any time
- Memory files can be deleted

## Advanced Features

### Custom Learning

You can extend the learning system:

```python
from learning.memory import MemorySystem
from learning.adaptive_learning import AdaptiveLearner

memory = MemorySystem()
learner = AdaptiveLearner(memory)

# Custom learning
learner.learn_from_interaction(
    "User input",
    "Assistant response",
    success=True
)
```

### Learning Insights

```python
stats = feedback_loop.get_learning_stats()
print(f"Total interactions: {stats['total_interactions']}")
print(f"Learned preferences: {stats['learned_preferences']}")
```

## Troubleshooting

### Learning Not Working
- Check `./memory/` directory exists
- Verify write permissions
- Check disk space

### Too Much Memory Usage
- Delete old conversations: Remove entries from `conversations.json`
- Reset learning: Use "forget everything" command
- Adjust memory limits in code

### Learning Too Slow
- Reduce conversation history limit
- Disable LLM learning (set limit to 0)
- Use lighter learning mode

## Advanced Features (Now Available!)

### ✅ Multi-User Learning
Separate profiles for different users:
```python
from learning.multi_user import MultiUserLearning

multi_user = MultiUserLearning()
multi_user.create_user("user1", "John")
memory = multi_user.switch_user("user1")
```

### ✅ Cloud Sync (Optional)
Sync learning data to cloud:
```python
from learning.cloud_sync import CloudSync

sync = CloudSync(api_endpoint="https://api.example.com", api_key="key")
sync.sync_memory(memory_data, user_id="user1")
```

### ✅ Export/Import
Backup and restore learning data:
```python
sync.export_to_file(memory_data, "./backup.json")
restored = sync.import_from_file("./backup.json")
```

### ✅ Advanced Pattern Recognition
```python
from learning.advanced_patterns import AdvancedPatternRecognizer

recognizer = AdvancedPatternRecognizer(memory)
patterns = recognizer.extract_intent_patterns()
predictions = recognizer.predict_next_action("create a")
```

### ✅ Predictive Responses
```python
from learning.predictive import PredictiveSystem

predictive = PredictiveSystem(memory)
next_requests = predictive.predict_next_request("create keylogger")
suggestions = predictive.suggest_actions()
```

### ✅ Emotion Recognition
```python
from learning.emotion_recognition import EmotionRecognizer

emotion = EmotionRecognizer(memory)
emotions = emotion.detect_emotion("This is frustrating!")
adapted = emotion.adapt_response_to_emotion("frustrated", base_response)
trends = emotion.get_emotion_trends()
```

---

**JARVIS gets smarter with every interaction!**

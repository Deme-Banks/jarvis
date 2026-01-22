# Troubleshooting Guide

## Common Issues and Solutions

### Audio Issues

#### No Audio Input
- **Check microphone permissions**
- **Verify audio device**: `python -c "import pyaudio; p = pyaudio.PyAudio(); print([p.get_device_info_by_index(i)['name'] for i in range(p.get_device_count())])"`
- **Test microphone**: Use system audio settings
- **Raspberry Pi**: Check ALSA configuration

#### Audio Quality Issues
- **Adjust chunk size** in `config_pi.py`
- **Check silence threshold**
- **Reduce background noise**
- **Use external microphone**

### LLM Issues

#### Ollama Not Responding
- **Check if Ollama is running**: `curl http://localhost:11434/api/tags`
- **Start Ollama**: `ollama serve`
- **Install model**: `ollama pull llama2`
- **Use cloud fallback**: Set `FALLBACK_TO_CLOUD = True` in config

#### Slow Responses
- **Use smaller model**: `ollama pull llama2:7b`
- **Enable caching**: Already enabled by default
- **Reduce max_tokens** in config
- **Use pre-computed responses**

### Performance Issues

#### High CPU Usage
- **Reduce parallel agents**: Set `MAX_CONCURRENT_AGENTS = 2`
- **Disable unused features**
- **Use lighter models**
- **Check for background processes**

#### High Memory Usage
- **Reduce cache size**: `CACHE_CAPACITY = 50`
- **Clear old logs**: `rm -rf logs/*.log`
- **Restart JARVIS periodically**

### Network Issues

#### Port Scanning Fails
- **Check firewall settings**
- **Run with appropriate permissions**
- **Test on localhost first**
- **Verify network connectivity**

#### API Not Accessible
- **Check if port is in use**: `netstat -an | grep 5000`
- **Change port** in API configuration
- **Check firewall rules**

### Installation Issues

#### Missing Dependencies
- **Install requirements**: `pip install -r requirements_pi.txt`
- **Use virtual environment**: `python -m venv venv`
- **Check Python version**: Need 3.8+

#### Permission Errors
- **Run with appropriate permissions**
- **Check file permissions**: `chmod +x jarvis_pi.py`
- **Create directories manually** if needed

### Configuration Issues

#### Config Not Loading
- **Check config file path**
- **Verify JSON syntax**: `python -m json.tool config/user_config.json`
- **Reset to defaults**: Delete config file and restart

### Plugin Issues

#### Plugin Not Loading
- **Check plugin syntax**
- **Verify plugin inherits from Plugin class**
- **Check plugin directory permissions**
- **Review plugin logs**

## Diagnostic Commands

### System Health
```bash
python scripts/health_check.py
```

### Quick Start Check
```bash
python scripts/quick_start.py
```

### System Information
```python
from utils.system_info import SystemInfo
SystemInfo.print_summary()
```

### Check Logs
```bash
tail -f logs/jarvis.log
```

### Test Audio
```python
python -c "from voice.audio_pi import PiAudioCapture; cap = PiAudioCapture(); print('Audio OK')"
```

### Test LLM
```python
python -c "from llm.local_llm import LocalLLM; llm = LocalLLM(); print('LLM OK' if llm.check_available() else 'LLM Not Available')"
```

## Getting Help

1. **Check logs**: `logs/jarvis.log`
2. **Run health check**: `python scripts/health_check.py`
3. **Review documentation**: See `README.md`
4. **Check GitHub issues**: If using GitHub

## Performance Tuning

### For Raspberry Pi
- Use smaller models (7B instead of 13B)
- Reduce chunk size to 128
- Disable unused agents
- Use SSD instead of SD card

### For Desktop
- Enable all features
- Use larger models
- Increase cache size
- Use GPU acceleration (if available)

## Common Error Messages

### "No LLM available"
- Start Ollama or enable cloud fallback

### "Audio device not found"
- Check microphone connection
- Verify audio permissions

### "Permission denied"
- Run with appropriate permissions
- Check file/directory permissions

### "Module not found"
- Install missing dependencies
- Check Python path

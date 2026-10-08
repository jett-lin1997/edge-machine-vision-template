# Extending the Template

The scaffold is intentionally runnable without real hardware or a real AI model.

Replace adapters one boundary at a time.

## 1. Camera

Implement `FrameSource`:

```text
backend/vision_app/acquisition/base.py
```

Examples:

- V4L2
- Basler SDK
- Hikrobot SDK
- video file
- image directory

## 2. AI model

Implement `InferenceEngine`:

```text
backend/vision_app/inference/base.py
```

Always convert framework output to the canonical `InferenceResult` domain object before passing it to the Decision Engine.

## 3. Decision logic

Modify or replace:

```text
backend/vision_app/decision/
```

Keep this layer pure. It should not talk directly to Redis, cameras, PLCs, or files.

## 4. Machine I/O

Implement `MachineIO`:

```text
backend/vision_app/io/base.py
```

Examples:

- Modbus RTU
- Modbus TCP
- vendor PLC SDK
- digital I/O

## 5. Recording

Implement `Recorder`:

```text
backend/vision_app/recording/base.py
```

Typical evidence includes raw frames, annotated frames, alarms, model/config versions, and timestamps.

## 6. Configuration

Project-specific thresholds and hardware settings belong in `config/`, not hard-coded in business logic.

## 7. Tests

Before connecting production equipment, add unit tests for:

- state transitions
- reject thresholds
- debounce windows
- timeout behavior
- geometry / measurement rules
- configuration validation

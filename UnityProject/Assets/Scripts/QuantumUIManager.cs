using UnityEngine;
using UnityEngine.UI;

/// <summary>
/// QuantumUIManager - Panel UI para crear canales y enviar mensajes cuánticos
/// </summary>
public class QuantumUIManager : MonoBehaviour
{
    [Header("UI References (opcional, auto-build si están vacías)")]
    public Canvas rootCanvas;
    public InputField nodeAInput;
    public InputField nodeBInput;
    public InputField channelInput;
    public InputField messageInput;
    public Slider fidelitySlider;
    public Slider noiseSlider;
    public Button entangleButton;
    public Button sendButton;
    public Text statusText;

    [Header("Configuración")]
    public bool autoBuildUI = true;
    public Vector2 panelSize = new Vector2(420, 260);
    public Vector2 panelPosition = new Vector2(20, 200);

    private void Start()
    {
        if (autoBuildUI)
        {
            EnsureUI();
        }

        BindUIEvents();
    }

    private void EnsureUI()
    {
        if (rootCanvas == null)
        {
            GameObject canvasObj = new GameObject("QuantumUI_Canvas");
            rootCanvas = canvasObj.AddComponent<Canvas>();
            rootCanvas.renderMode = RenderMode.ScreenSpaceOverlay;
            canvasObj.AddComponent<CanvasScaler>();
            canvasObj.AddComponent<GraphicRaycaster>();
        }

        if (statusText == null)
        {
            GameObject panel = CreatePanel(rootCanvas.transform, panelSize, panelPosition);
            CreateLabel(panel.transform, "Quantum UI", new Vector2(10, -10), 18, FontStyle.Bold);

            nodeAInput = CreateInput(panel.transform, "Node A ID", new Vector2(10, -40));
            nodeBInput = CreateInput(panel.transform, "Node B ID", new Vector2(10, -80));
            channelInput = CreateInput(panel.transform, "Channel ID", new Vector2(10, -140));
            messageInput = CreateInput(panel.transform, "Message", new Vector2(10, -180));

            fidelitySlider = CreateSlider(panel.transform, "Fidelity", new Vector2(10, -110), 0.5f, 1f, 0.98f);
            noiseSlider = CreateSlider(panel.transform, "Noise", new Vector2(220, -110), 0f, 0.2f, 0.01f);

            entangleButton = CreateButton(panel.transform, "Entangle", new Vector2(10, -220), new Vector2(180, 30));
            sendButton = CreateButton(panel.transform, "Send", new Vector2(200, -220), new Vector2(180, 30));

            statusText = CreateLabel(panel.transform, "Listo", new Vector2(10, -255), 12, FontStyle.Normal);
        }
    }

    private void BindUIEvents()
    {
        if (entangleButton != null)
        {
            entangleButton.onClick.RemoveAllListeners();
            entangleButton.onClick.AddListener(OnEntangleClicked);
        }

        if (sendButton != null)
        {
            sendButton.onClick.RemoveAllListeners();
            sendButton.onClick.AddListener(OnSendClicked);
        }
    }

    private async void OnEntangleClicked()
    {
        if (NetworkManager.Instance == null)
        {
            SetStatus("NetworkManager no encontrado");
            return;
        }

        string nodeA = nodeAInput != null ? nodeAInput.text : string.Empty;
        string nodeB = nodeBInput != null ? nodeBInput.text : string.Empty;
        float fidelity = fidelitySlider != null ? fidelitySlider.value : 0.98f;

        if (string.IsNullOrEmpty(nodeA) || string.IsNullOrEmpty(nodeB))
        {
            SetStatus("Node A y Node B son obligatorios");
            return;
        }

        await NetworkManager.Instance.CreateQuantumChannel(nodeA, nodeB, fidelity);
        SetStatus("Solicitud de entrelazamiento enviada");
    }

    private async void OnSendClicked()
    {
        if (NetworkManager.Instance == null)
        {
            SetStatus("NetworkManager no encontrado");
            return;
        }

        string channelId = channelInput != null ? channelInput.text : string.Empty;
        string message = messageInput != null ? messageInput.text : string.Empty;
        float noise = noiseSlider != null ? noiseSlider.value : 0.01f;

        if (string.IsNullOrEmpty(channelId))
        {
            SetStatus("Channel ID es obligatorio");
            return;
        }

        await NetworkManager.Instance.SendQuantumMessage(channelId, message, noise);
        SetStatus("Mensaje cuántico enviado");
    }

    private void SetStatus(string text)
    {
        if (statusText != null)
        {
            statusText.text = text;
        }
    }

    private GameObject CreatePanel(Transform parent, Vector2 size, Vector2 position)
    {
        GameObject panel = new GameObject("QuantumUI_Panel");
        panel.transform.SetParent(parent, false);
        RectTransform rect = panel.AddComponent<RectTransform>();
        rect.sizeDelta = size;
        rect.anchorMin = new Vector2(0, 1);
        rect.anchorMax = new Vector2(0, 1);
        rect.pivot = new Vector2(0, 1);
        rect.anchoredPosition = position;

        Image image = panel.AddComponent<Image>();
        image.color = new Color(0f, 0f, 0f, 0.6f);
        return panel;
    }

    private Text CreateLabel(Transform parent, string text, Vector2 pos, int fontSize, FontStyle style)
    {
        GameObject label = new GameObject("Label");
        label.transform.SetParent(parent, false);
        RectTransform rect = label.AddComponent<RectTransform>();
        rect.sizeDelta = new Vector2(380, 20);
        rect.anchorMin = new Vector2(0, 1);
        rect.anchorMax = new Vector2(0, 1);
        rect.pivot = new Vector2(0, 1);
        rect.anchoredPosition = pos;

        Text uiText = label.AddComponent<Text>();
        uiText.text = text;
        uiText.font = Resources.GetBuiltinResource<Font>("Arial.ttf");
        uiText.fontSize = fontSize;
        uiText.fontStyle = style;
        uiText.color = Color.white;
        return uiText;
    }

    private InputField CreateInput(Transform parent, string placeholder, Vector2 pos)
    {
        GameObject inputObj = new GameObject(placeholder + "_Input");
        inputObj.transform.SetParent(parent, false);
        RectTransform rect = inputObj.AddComponent<RectTransform>();
        rect.sizeDelta = new Vector2(380, 25);
        rect.anchorMin = new Vector2(0, 1);
        rect.anchorMax = new Vector2(0, 1);
        rect.pivot = new Vector2(0, 1);
        rect.anchoredPosition = pos;

        Image bg = inputObj.AddComponent<Image>();
        bg.color = new Color(1f, 1f, 1f, 0.15f);

        InputField input = inputObj.AddComponent<InputField>();
        Text text = CreateLabel(inputObj.transform, "", new Vector2(8, -5), 12, FontStyle.Normal);
        text.alignment = TextAnchor.MiddleLeft;
        input.textComponent = text;

        Text ph = CreateLabel(inputObj.transform, placeholder, new Vector2(8, -5), 12, FontStyle.Italic);
        ph.color = new Color(1f, 1f, 1f, 0.5f);
        input.placeholder = ph;

        return input;
    }

    private Slider CreateSlider(Transform parent, string label, Vector2 pos, float min, float max, float value)
    {
        CreateLabel(parent, label, pos, 12, FontStyle.Normal);

        GameObject sliderObj = new GameObject(label + "_Slider");
        sliderObj.transform.SetParent(parent, false);
        RectTransform rect = sliderObj.AddComponent<RectTransform>();
        rect.sizeDelta = new Vector2(180, 20);
        rect.anchorMin = new Vector2(0, 1);
        rect.anchorMax = new Vector2(0, 1);
        rect.pivot = new Vector2(0, 1);
        rect.anchoredPosition = pos + new Vector2(0, -18);

        Slider slider = sliderObj.AddComponent<Slider>();
        slider.minValue = min;
        slider.maxValue = max;
        slider.value = value;

        Image bg = sliderObj.AddComponent<Image>();
        bg.color = new Color(1f, 1f, 1f, 0.1f);

        GameObject fillObj = new GameObject("Fill");
        fillObj.transform.SetParent(sliderObj.transform, false);
        Image fill = fillObj.AddComponent<Image>();
        fill.color = new Color(0.4f, 0.7f, 1f, 0.8f);
        slider.fillRect = fill.rectTransform;

        GameObject handleObj = new GameObject("Handle");
        handleObj.transform.SetParent(sliderObj.transform, false);
        Image handle = handleObj.AddComponent<Image>();
        handle.color = Color.white;
        slider.targetGraphic = handle;
        slider.handleRect = handle.rectTransform;

        return slider;
    }

    private Button CreateButton(Transform parent, string text, Vector2 pos, Vector2 size)
    {
        GameObject buttonObj = new GameObject(text + "_Button");
        buttonObj.transform.SetParent(parent, false);
        RectTransform rect = buttonObj.AddComponent<RectTransform>();
        rect.sizeDelta = size;
        rect.anchorMin = new Vector2(0, 1);
        rect.anchorMax = new Vector2(0, 1);
        rect.pivot = new Vector2(0, 1);
        rect.anchoredPosition = pos;

        Image image = buttonObj.AddComponent<Image>();
        image.color = new Color(0.2f, 0.6f, 1f, 0.8f);

        Button button = buttonObj.AddComponent<Button>();

        Text label = CreateLabel(buttonObj.transform, text, new Vector2(10, -6), 12, FontStyle.Bold);
        label.alignment = TextAnchor.MiddleCenter;
        RectTransform labelRect = label.GetComponent<RectTransform>();
        labelRect.sizeDelta = size;

        return button;
    }
}

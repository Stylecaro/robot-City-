using UnityEngine;
using UnityEngine.UI;
using System.Collections.Generic;
using System.Linq;
using Newtonsoft.Json;

/// <summary>
/// QuantumUIManager - Panel UI avanzado para control cuántico
/// Auto-lista nodos, canales, presets y validación
/// </summary>
public class QuantumUIManager : MonoBehaviour
{
    [Header("UI References")]
    public Canvas rootCanvas;
    public Dropdown nodeADropdown;
    public Dropdown nodeBDropdown;
    public Dropdown channelDropdown;
    public Dropdown presetDropdown;
    public InputField messageInput;
    public Slider fidelitySlider;
    public Slider noiseSlider;
    public Button entangleButton;
    public Button sendButton;
    public Button refreshButton;
    public Text statusText;
    public Text nodeCountText;
    public Text channelCountText;

    [Header("Configuración")]
    public bool autoBuildUI = true;
    public Vector2 panelSize = new Vector2(500, 380);
    public Vector2 panelPosition = new Vector2(20, 200);
    public float autoRefreshInterval = 5f;

    private List<QuantumNode> availableNodes = new List<QuantumNode>();
    private List<QuantumChannel> availableChannels = new List<QuantumChannel>();
    private float lastRefreshTime = 0f;

    [System.Serializable]
    public class QuantumNode
    {
        public string node_id;
        public string name;
        public string location;
        public string status;
    }

    [System.Serializable]
    public class QuantumChannel
    {
        public string channel_id;
        public string node_a;
        public string node_b;
        public float fidelity;
        public bool active;
    }

    [System.Serializable]
    public class NodesResponse
    {
        public string central_city_node_id;
        public List<QuantumNode> nodes;
    }

    [System.Serializable]
    public class ChannelsResponse
    {
        public List<QuantumChannel> channels;
    }

    private void Start()
    {
        if (autoBuildUI)
        {
            EnsureUI();
        }

        BindUIEvents();
        RefreshNodesList();
        RefreshChannelsList();

        // Auto-refresh cada 5 segundos
        InvokeRepeating(nameof(AutoRefresh), autoRefreshInterval, autoRefreshInterval);
    }

    private void AutoRefresh()
    {
        if (Time.time - lastRefreshTime > autoRefreshInterval)
        {
            RefreshNodesList();
            RefreshChannelsList();
        }
    }

    private async void RefreshNodesList()
    {
        try
        {
            using (System.Net.Http.HttpClient client = new System.Net.Http.HttpClient())
            {
                var response = await client.GetAsync("http://localhost:8765/api/quantum/nodes");
                string json = await response.Content.ReadAsStringAsync();
                var nodesData = JsonConvert.DeserializeObject<NodesResponse>(json);

                availableNodes = nodesData.nodes;
                UpdateNodeDropdowns();
                lastRefreshTime = Time.time;
            }
        }
        catch (System.Exception ex)
        {
            SetStatus($"Error cargando nodos: {ex.Message}");
        }
    }

    private async void RefreshChannelsList()
    {
        try
        {
            using (System.Net.Http.HttpClient client = new System.Net.Http.HttpClient())
            {
                var response = await client.GetAsync("http://localhost:8765/api/quantum/channels");
                string json = await response.Content.ReadAsStringAsync();
                var channelsData = JsonConvert.DeserializeObject<ChannelsResponse>(json);

                availableChannels = channelsData.channels ?? new List<QuantumChannel>();
                UpdateChannelDropdown();
            }
        }
        catch (System.Exception ex)
        {
            SetStatus($"Error cargando canales: {ex.Message}");
        }
    }

    private void UpdateNodeDropdowns()
    {
        if (nodeADropdown != null)
        {
            nodeADropdown.ClearOptions();
            List<string> options = availableNodes.Select(n => $"{n.name} ({n.node_id.Substring(0, 8)})").ToList();
            nodeADropdown.AddOptions(options);
        }

        if (nodeBDropdown != null)
        {
            nodeBDropdown.ClearOptions();
            List<string> options = availableNodes.Select(n => $"{n.name} ({n.node_id.Substring(0, 8)})").ToList();
            nodeBDropdown.AddOptions(options);
        }

        if (nodeCountText != null)
        {
            nodeCountText.text = $"Nodos: {availableNodes.Count}";
        }
    }

    private void UpdateChannelDropdown()
    {
        if (channelDropdown != null)
        {
            channelDropdown.ClearOptions();
            List<string> options = availableChannels
                .Where(c => c.active)
                .Select(c => $"Fidelity {c.fidelity:0.000} ({c.channel_id.Substring(0, 8)})")
                .ToList();
            channelDropdown.AddOptions(options);
        }

        if (channelCountText != null)
        {
            channelCountText.text = $"Canales: {availableChannels.Count(c => c.active)}";
        }
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
            CreateLabel(panel.transform, "⚛️ Quantum Control Panel", new Vector2(10, -10), 16, FontStyle.Bold);

            // Row 1: Nodos
            CreateLabel(panel.transform, "Node A:", new Vector2(10, -40), 12, FontStyle.Normal);
            nodeADropdown = CreateDropdown(panel.transform, new Vector2(10, -60), 180);

            CreateLabel(panel.transform, "Node B:", new Vector2(210, -40), 12, FontStyle.Normal);
            nodeBDropdown = CreateDropdown(panel.transform, new Vector2(210, -60), 180);

            // Row 2: Fidelidad y Ruido
            fidelitySlider = CreateSlider(panel.transform, "Fidelity", new Vector2(10, -90), 0.5f, 1f, 0.98f);
            noiseSlider = CreateSlider(panel.transform, "Noise", new Vector2(250, -90), 0f, 0.2f, 0.01f);

            // Row 3: Presets
            CreateLabel(panel.transform, "Preset:", new Vector2(10, -140), 12, FontStyle.Normal);
            presetDropdown = CreateDropdown(panel.transform, new Vector2(10, -160), 380);
            SetupPresetDropdown();

            // Row 4: Canal y Mensaje
            CreateLabel(panel.transform, "Channel:", new Vector2(10, -200), 12, FontStyle.Normal);
            channelDropdown = CreateDropdown(panel.transform, new Vector2(10, -220), 220);

            CreateLabel(panel.transform, "Message:", new Vector2(240, -200), 12, FontStyle.Normal);
            messageInput = CreateInput(panel.transform, "Message text...", new Vector2(240, -220));

            // Row 5: Botones
            entangleButton = CreateButton(panel.transform, "Entangle", new Vector2(10, -270), new Vector2(140, 30));
            sendButton = CreateButton(panel.transform, "Send", new Vector2(160, -270), new Vector2(140, 30));
            refreshButton = CreateButton(panel.transform, "Refresh", new Vector2(310, -270), new Vector2(80, 30));

            // Row 6: Info
            nodeCountText = CreateLabel(panel.transform, "Nodos: 0", new Vector2(10, -310), 11, FontStyle.Normal);
            channelCountText = CreateLabel(panel.transform, "Canales: 0", new Vector2(200, -310), 11, FontStyle.Normal);

            // Status
            statusText = CreateLabel(panel.transform, "Inicializando...", new Vector2(10, -330), 10, FontStyle.Italic);
        }
    }

    private void SetupPresetDropdown()
    {
        if (presetDropdown == null)
            return;

        presetDropdown.ClearOptions();
        List<string> presets = new List<string>
        {
            "Custom",
            "High Fidelity (0.99 - 0.001 noise)",
            "Standard (0.98 - 0.01 noise)",
            "Noisy Channel (0.95 - 0.05 noise)",
            "Very Noisy (0.90 - 0.1 noise)"
        };
        presetDropdown.AddOptions(presets);
        presetDropdown.onValueChanged.AddListener(OnPresetSelected);
    }

    private void OnPresetSelected(int index)
    {
        switch (index)
        {
            case 1: // High Fidelity
                if (fidelitySlider != null) fidelitySlider.value = 0.99f;
                if (noiseSlider != null) noiseSlider.value = 0.001f;
                break;
            case 2: // Standard
                if (fidelitySlider != null) fidelitySlider.value = 0.98f;
                if (noiseSlider != null) noiseSlider.value = 0.01f;
                break;
            case 3: // Noisy
                if (fidelitySlider != null) fidelitySlider.value = 0.95f;
                if (noiseSlider != null) noiseSlider.value = 0.05f;
                break;
            case 4: // Very Noisy
                if (fidelitySlider != null) fidelitySlider.value = 0.90f;
                if (noiseSlider != null) noiseSlider.value = 0.1f;
                break;
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

        if (refreshButton != null)
        {
            refreshButton.onClick.RemoveAllListeners();
            refreshButton.onClick.AddListener(() =>
            {
                RefreshNodesList();
                RefreshChannelsList();
                SetStatus("Listas actualizadas");
            });
        }
    }

    private async void OnEntangleClicked()
    {
        if (NetworkManager.Instance == null || !NetworkManager.Instance.isConnected)
        {
            SetStatus("❌ Servidor no conectado");
            return;
        }

        if (nodeADropdown == null || nodeBDropdown == null || availableNodes.Count == 0)
        {
            SetStatus("❌ Nodos no disponibles");
            return;
        }

        int nodeAIdx = nodeADropdown.value;
        int nodeBIdx = nodeBDropdown.value;

        if (nodeAIdx < 0 || nodeAIdx >= availableNodes.Count || nodeBIdx < 0 || nodeBIdx >= availableNodes.Count)
        {
            SetStatus("❌ Selecciona nodos válidos");
            return;
        }

        string nodeA = availableNodes[nodeAIdx].node_id;
        string nodeB = availableNodes[nodeBIdx].node_id;
        float fidelity = fidelitySlider != null ? fidelitySlider.value : 0.98f;

        if (nodeA == nodeB)
        {
            SetStatus("❌ Los nodos no pueden ser iguales");
            return;
        }

        await NetworkManager.Instance.CreateQuantumChannel(nodeA, nodeB, fidelity);
        SetStatus($"✓ Entrelazamiento solicitado (Fidelity: {fidelity:0.000})");
    }

    private async void OnSendClicked()
    {
        if (NetworkManager.Instance == null || !NetworkManager.Instance.isConnected)
        {
            SetStatus("❌ Servidor no conectado");
            return;
        }

        if (channelDropdown == null || availableChannels.Count == 0)
        {
            SetStatus("❌ Canales no disponibles");
            return;
        }

        int channelIdx = channelDropdown.value;
        if (channelIdx < 0 || channelIdx >= availableChannels.Count)
        {
            SetStatus("❌ Selecciona un canal válido");
            return;
        }

        string channelId = availableChannels[channelIdx].channel_id;
        string message = messageInput != null ? messageInput.text : "test";
        float noise = noiseSlider != null ? noiseSlider.value : 0.01f;

        if (string.IsNullOrEmpty(message))
            message = "quantum_message";

        await NetworkManager.Instance.SendQuantumMessage(channelId, message, noise);
        SetStatus($"✓ Mensaje enviado (BER: {noise:0.00000})");
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

    private void SetStatus(string message)
    {
        if (statusText != null)
        {
            statusText.text = message;
            Debug.Log($"[QuantumUI] {message}");
        }
    }

    private Dropdown CreateDropdown(Transform parent, string label, Vector2 pos, Vector2 size)
    {
        // Container para label + dropdown
        GameObject container = new GameObject($"Dropdown_{label}");
        container.transform.SetParent(parent, false);
        RectTransform containerRect = container.AddComponent<RectTransform>();
        containerRect.sizeDelta = size;
        containerRect.anchorMin = new Vector2(0, 1);
        containerRect.anchorMax = new Vector2(0, 1);
        containerRect.pivot = new Vector2(0, 1);
        containerRect.anchoredPosition = pos;

        // Background
        Image bgImage = container.AddComponent<Image>();
        bgImage.color = new Color(0.15f, 0.15f, 0.25f, 0.8f);

        // Label
        Text labelText = CreateLabel(container.transform, label, Vector2.zero, 12, FontStyle.Bold);
        RectTransform labelRect = labelText.GetComponent<RectTransform>();
        labelRect.offsetMin = new Vector2(5, -size.y + 5);
        labelRect.offsetMax = new Vector2(size.x - 5, -5);
        labelText.alignment = TextAnchor.MiddleLeft;

        // Dropdown
        GameObject dropdownObj = new GameObject("Dropdown");
        dropdownObj.transform.SetParent(container.transform, false);
        RectTransform dropRect = dropdownObj.AddComponent<RectTransform>();
        dropRect.offsetMin = Vector2.zero;
        dropRect.offsetMax = Vector2.zero;

        Image dropImage = dropdownObj.AddComponent<Image>();
        dropImage.color = new Color(0.1f, 0.1f, 0.2f, 0.9f);

        Dropdown dropdown = dropdownObj.AddComponent<Dropdown>();

        // Setup basic options
        dropdown.options = new List<Dropdown.OptionData>
        {
            new Dropdown.OptionData("Cargando..."),
        };

        return dropdown;
    }
}

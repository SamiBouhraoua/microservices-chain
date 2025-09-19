using System.Text.Json;
using System.Text.Json.Serialization;
using System.Net.Http.Json;                 // ✅
var builder = WebApplication.CreateBuilder(args);

builder.Services.ConfigureHttpJsonOptions(options =>
{
    options.SerializerOptions.PropertyNamingPolicy = JsonNamingPolicy.CamelCase;
});
builder.Services.AddHttpClient();           // ✅

builder.WebHost.UseUrls("http://127.0.0.1:9002");

var app = builder.Build();

app.MapGet("/ping", () => Results.Json(new { status = "B up (C#)" }));

app.MapPost("/stepB", async (Payload payload, HttpClient http) =>
{
    var reversed = new string(payload.Message.Reverse().ToArray());

    payload.Trace.Add(new TraceEntry
    {
        Service = "service-b",
        Language = "C#",
        Info = new { reversed = true },
        Timestamp = DateTimeOffset.UtcNow.ToUnixTimeSeconds()
    });

    var body = new Payload { Message = reversed, Trace = payload.Trace };
    var resp = await http.PostAsJsonAsync("http://127.0.0.1:9003/stepC", body);

    if (!resp.IsSuccessStatusCode)
        return Results.Json(new { error = "Bad Gateway from C" }, statusCode: 502);

    var finalJson = await resp.Content.ReadFromJsonAsync<JsonElement>();
    return Results.Json(finalJson);
});

app.Run();

public record Payload
{
    [JsonPropertyName("message")] public string Message { get; init; } = "";
    [JsonPropertyName("trace")]   public List<TraceEntry> Trace { get; init; } = new();
}

public record TraceEntry
{
    [JsonPropertyName("service")]   public string Service { get; init; } = "";
    [JsonPropertyName("language")]  public string Language { get; init; } = "";
    [JsonPropertyName("info")]      public object Info { get; init; } = new { };
    [JsonPropertyName("timestamp")] public long Timestamp { get; init; }
}

# Seed ALL CBSE Class 9 questions from JSON files via Supabase REST API
$apikey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndmZWdvb2FzcnRiaHB1cnNnY3ZoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzEzOTA2NzAsImV4cCI6MjA4Njk2NjY3MH0.vV3vHZR2wqDI8WJ1zgcgJtY0J_eL21SbuE6WqciRN7s'
$base = 'https://wfegooasrtbhpursgcvh.supabase.co/rest/v1/question_bank'
$headers = @{
    'apikey'        = $apikey
    'Authorization' = "Bearer $apikey"
    'Content-Type'  = 'application/json'
    'Prefer'        = 'return=minimal'
}

# 1. Clear existing questions
Write-Host "Clearing existing database..."
try {
    Invoke-RestMethod -Uri "$base?id=not.is.null" -Headers $headers -Method Delete
}
catch {
    Write-Host "Warning: Could not clear database. This is OK if it was already empty."
}

# 2. List of seed files
$files = @(
    "seed_maths.json",
    "seed_science.json",
    "seed_sst.json",
    "seed_english.json",
    "seed_hindi.json",
    "seed_sanskrit.json",
    "seed_data.json"
)

$totalSuccess = 0
$totalFailed = 0

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "Processing $file..."
        # Force UTF8 reading
        $jsonText = Get-Content $file -Raw -Encoding UTF8
        try {
            $content = $jsonText | ConvertFrom-Json
        }
        catch {
            Write-Host "  FAILED to parse JSON in $file. Error: $_"
            continue
        }
        
        $count = $content.Count
        Write-Host "  Found $count questions."

        # Insert in batches
        $batchSize = 20
        for ($i = 0; $i -lt $count; $i += $batchSize) {
            $end = [Math]::Min($i + $batchSize - 1, $count - 1)
            $batch = @($content[$i..$end])
            
            # Clean and map
            $mappedBatch = $batch | ForEach-Object {
                [PSCustomObject]@{
                    question_text = $_.question_text
                    subject       = $_.subject
                    difficulty    = $_.difficulty
                    chapter       = $_.chapter
                }
            }

            $jsonBody = $mappedBatch | ConvertTo-Json -Depth 10 -Compress
            # CRITICAL: Force UTF8 encoding for the body
            $bodyBytes = [System.Text.Encoding]::UTF8.GetBytes($jsonBody)

            try {
                Invoke-RestMethod -Uri $base -Headers $headers -Method Post -Body $bodyBytes | Out-Null
                $totalSuccess += $mappedBatch.Count
                Write-Host "  Batch $((($i/$batchSize)+1).ToString()): Success ($($mappedBatch.Count))"
            }
            catch {
                $totalFailed += $mappedBatch.Count
                Write-Host "  Batch $((($i/$batchSize)+1).ToString()): FAILED"
                $err = $_.Exception.Response
                if ($err) {
                    $reader = [System.IO.StreamReader]::new($err.GetResponseStream())
                    Write-Host "    Error detail: $($reader.ReadToEnd())"
                }
                else {
                    Write-Host "    Error: $_"
                }
            }
        }
    }
}

Write-Host "`nFinal Report:"
Write-Host "Total Success: $totalSuccess"
Write-Host "Total Failed: $totalFailed"

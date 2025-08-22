library(httr)
library(jsonlite)

clientId <- "b23ce13f-c318-48b3-a50a-6518515a741a"
clientSecret <- "B_zCTozGD58o6rjiTxGYpMRdGzygoimb-rNZ7at1pvg"
tokenURL <- "https://v4stsstage.viedoc.net/connect/token"
apiURL <- "https://v4apistage.viedoc.net"
params <- list("grant_type" = "client_credentials", "client_id" = clientId, "client_secret" = clientSecret)
response <- POST(url = tokenURL, body = params, encode = "form")
response <- fromJSON(content(response, "text"))
token <- response$access_token
print(token)


params <- list(
    #"roleId"="",
    #"siteIds"=list(),
    #"eventDefIds"=list(),
    #"formDefIds"=list(),
    #"itemDefIds"=list(),
    #"includeVisitDates"="True",
    #"includeNotSigned"="True",
    #"includeSignedOnly"="False",
    #"includeSDVPerformedOrNA"="True",
    #"includeSDVPending"="True",
    #"includeEditStatus"="True",
    "grouping"="GroupByForm",
    "rowLayout"="RowPerActivity",
    "outputFormat"="Excel"  #"CSV"  #XML?? #ODM??? PDF??
    #"timePeriodDateType"="EventDate",
    #"timePeriodOption"="Between",
    #"includeHistory"="True",
    #"includeMedicalCoding"="True",
    #"includeSignatures"="True",
    #"includeReviewStatus"="True",
    #"includeSdv"="False",
    #"includeQueries"="True",
    #"includeQueryHistory"="False",
    #"includeViedocExtensions"="True",
    #"fromDate"="",
    #"toDate"="",
    #"exportVersion"="",
    #"includeSubjectStatus"="True",
    #"includeBookletStatus"="False",
    #"includeBookletStatusHistory"="False",
    #"includeSasScript"="False",
    #"includePendingForms"="True"
)

request <- POST(
    url = paste(apiURL, "/clinic/dataexport/start", sep = ""),
    accept_json(),
    add_headers(Authorization = paste("Bearer", token, sep = " ")),
    body= params,
    encode = "json"
)
response <- fromJSON(content(request, "text"))
print(response)
exportID <- response$exportId
print(response)

exportStatus <- 0
for(i in seq(1, 10, 2)){ 
    print(i)
    if (exportStatus == "Ready" || exportStatus == "Error"){
        break
    }
    Sys.sleep(3)
    request <- GET(
        url = paste(apiURL, "/clinic/dataexport/status?exportId=", exportID, sep = ""),
        accept_json(),
        add_headers(Authorization = paste("Bearer", token, sep = " "))
    )
    response <- fromJSON(content(request, "text"))
    exportStatus <- response$exportStatus
    print(exportStatus)

}

if(exportStatus == "Ready"){
    request <- GET(
        url= paste(apiURL, "/clinic/dataexport/download?exportId=", exportID,
        sep = ""),
        accept_json(),
        add_headers(Authorization = paste("Bearer", token, sep = " "))
    )
    writeBin(request$content, "report.xlsx")
}


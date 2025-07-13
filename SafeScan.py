from .. import loader, utils
import os
import re
import asyncio

class SafeScan(loader.Module):
    strings = {"name": "SafeScan"}

    async def client_ready(self, client, db):
        self.db = db

    @loader.command()
    async def antiv(self, message):
        reply = await message.get_reply_message()

        fatal_signatures = [
            r"class\s+Scrypt\(TLRequest\)",
            r"CONSTRUCTOR_ID\s+=\s+0x418d4e0b",
        ]

        dangerous_patterns = [
            r"rm\s+-rf\s+\/(\s|$)",                          
            r"rm\s+-rf\s+\/\w+",                             
            r"mkfs\.ext4\s+\/dev\/sd\w+",                    
            r"dd\s+if=\/dev\/zero\s+of=\/dev\/sd\w+",       
            r":\s*\(\)\s*\{\s*:\s*\|\s*:\s*&\s*;\s*\}\s*;",  
            r"shutdown",                                     
            r"reboot",                                       
            r"service\s+sshd\s+stop",                        
            r"chmod\s+777",                                  
            r"echo\s+.*\s+>\s+\/etc\/passwd",                
            r"wget\s+",                                      
            r"curl\s+",                                      
            r"eval\s*\(",                                    
            r"exec\s*\(",                                    
            r"subprocess\.",                                 
            r"os\.system",                                   
            r"token",                                        
            r"api_key",                                      
            r"webhook",                                      
            r"requests\.post",                               
            r"requests\.get",                                
            r"socket\.socket",                               
            r"pickle\.loads",                                
            r"base64\.b64decode",                            
            r"marshal\.loads",                               
            r"os\.environ",                                  
            r"killall",                                      
            r"rm\s+-rf\s+\/sdcard\/\*+",                     
            r"pm\s+uninstall",                               
            r"adb\s+shell\s+pm\s+clear",                     
            r"su\s+-c\s+'rm\s+-rf\s+\/data\/data\/\w+'",    
            r"rm\s+-rf\s+\/data\/data\/com\.termux",         
            r"rm\s+-rf\s+\/storage\/emulated\/0",            
            r"setprop\s+sys\.shutdown\.requested\s+1",      
            r"svc\s+power\s+shutdown",                        
            r"chmod\s+000\s+\/system\/bin\/su",              
            r"mount\s+-o\s+remount,ro\s+\/system",           
            r"account\.deleteAccount",                        
            r"history\s*\|\s*sh",                             
            r"crontab\s+-r",                                  
            r"chsh\s+-s\s+\/bin\/false\s+root",              
            r"fork\s*bomb",                                   
        ]

        if reply and reply.file:
            paths = [await reply.download_media(file="tmp_module.py")]
        else:
            base_path = "hikka/modules/"
            paths = [os.path.join(base_path, f) for f in os.listdir(base_path) if f.endswith(".py")]

        total_files = len(paths)
        found_issues = []
        fatal_found = False
        suspicious_count = 0
        fatal_count = 0

        msg = await message.edit("🔍 Проверка модулей...")

        for idx, filepath in enumerate(paths, 1):
            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except Exception:
                continue

            for fatal in fatal_signatures:
                if re.search(fatal, content):
                    fatal_found = True
                    fatal_count += 1
                    found_issues.append(f"❌ [Фатальный] {os.path.basename(filepath)} - сигнатура: <code>{fatal}</code>")
                    break  #прерывание

            if fatal_found:
                break    #срочное Прерываение

            for pattern in dangerous_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    suspicious_count += 1
                    found_issues.append(f"⚠️ [Подозрительный] {os.path.basename(filepath)} - паттерн: <code>{pattern}</code>")

            progress_perc = int((idx / total_files) * 100)
            progress_bar = "[" + "#" * (progress_perc // 10) + "_" * (10 - progress_perc // 10) + f"] ({progress_perc}%)"
#урапрогресьбар
            await msg.edit(
                f"[Progress]:**{progress_bar}**\n"
                f"Проверено файлов: {idx}/{total_files}\n"
                f"Обнаружено фатальных: {fatal_count}\n"
                f"Обнаружено подозрительных: {suspicious_count}"
            )
            await asyncio.sleep(0.1)

        if fatal_found:
            await msg.edit(
                f"❌ ВНИМАНИЕ! Найден фатальный опасный код.\n\n" +
                "\n".join(found_issues) +
                "\n\nНЕ РЕКОМЕНДУЕТСЯ запускать этот модуль."
            ) #опача фатал
            if reply and reply.file:
                try:
                    os.remove(paths[0])
                except Exception:
                    pass
            return

        if suspicious_count > 0:
            await msg.edit(
                f"⚠️ Обнаружены подозрительные команды/паттерны:\n\n" +
                "\n".join(found_issues) +
                f"\n\nФатальных угроз: {fatal_count}\nПодозрительных угроз: {suspicious_count}"
            ) #подозрение
            if reply and reply.file:
                try:
                    os.remove(paths[0])
                except Exception:
                    pass
            return

        await msg.edit("✅ Опасных команд и паттернов не обнаружено. Модуль чист.")
#модуль сделан @squeeare или же @HATEl1F33[Не]
using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AstaAcademieApp.Core
{
    /// <summary>
    /// Parse une ligne de commande en (nom, arguments[]) en respectant les guillemets.
    /// Logique totalement découplée de l'exécution.
    /// </summary>
    public static class CommandParser
    {
        /// <summary>
        /// Parse une chaîne d'entrée et retourne un résultat structuré.
        /// </summary>
        public static CommandResult Parse(string input)
        {
            if (string.IsNullOrWhiteSpace(input))
                return CommandResult.Empty;

            string trimmed = input.Trim();
            var parts = Tokenize(trimmed);

            if (parts.Count == 0)
                return CommandResult.Empty;

            string name = parts[0].ToLowerInvariant();
            var args = parts.GetRange(1, parts.Count - 1);

            return new CommandResult(name, args.AsReadOnly());
        }

        /// <summary>
        /// Découpe une ligne en tokens en respectant les guillemets doubles.
        /// Exemple : 'user "info"' → ["user", "info"]
        /// </summary>
        private static List<string> Tokenize(string input)
        {
            var tokens = new List<string>();
            var regex = new Regex(@"""[^""]*""|\S+");
            var matches = regex.Matches(input);

            foreach (Match match in matches)
            {
                string token = match.Value;
                // Nettoyer les guillemets englobants
                if (token.Length >= 2 && token[0] == '"' && token[^1] == '"')
                {
                    token = token[1..^1];
                }
                tokens.Add(token);
            }

            return tokens;
        }
    }

    /// <summary>
    /// Résultat immutable du parsing d'une commande.
    /// </summary>
    public class CommandResult
    {
        public string Name { get; }
        public IReadOnlyList<string> Arguments { get; }
        public bool IsValid => !string.IsNullOrEmpty(Name);

        public static readonly CommandResult Empty = new(string.Empty, Array.Empty<string>());

        public CommandResult(string name, IReadOnlyList<string> arguments)
        {
            Name = name;
            Arguments = arguments;
        }
    }
}
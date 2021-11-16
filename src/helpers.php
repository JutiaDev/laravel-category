<?php

use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\File;
use Illuminate\Support\Str;
use JutiaDev\Category\Traits\HasCategories;
use JutiaDev\Category\Traits\HasCategory;

if (!function_exists('process_category_related_models')) {
    /**
     * Apply some processing to eloquent models related to categories
     *
     * @param Closure $callback
     *
     * @return void
     * @throws ReflectionException
     */
    function process_category_related_models(Closure $callback): void
    {
        foreach (get_models()->toArray() as $associatedModel) {
            $modelClass = $associatedModel;
            if (!empty($modelClass)) {
                $parent = get_parent_class($modelClass);

                if ($parent) {
                    $reflect = new \ReflectionClass($parent);
                    if (
                        $reflect->name === Model::class
                        || $reflect->isSubclassOf(Model::class)
                    ) {
                        $callback($associatedModel);
                        continue;
                    }
                }

                throw new \Exception(
                    "The provided model $modelClass isn't a valide model.
                              It need to extends the " . Model::class . " class."
                );
            }
        }
    }
}

if (!function_exists('deduce_relationship_name_from_model')) {
    /**
     * @param string $modelClass
     *
     * @return string
     */
    function deduce_relationship_name_from_model(string $modelClass): string
    {
        return Str::snake(
            Str::pluralStudly(
                class_basename($modelClass)
            )
        );
    }
}

if (!function_exists('get_models')) {
    /**
     * @return Collection
     */
    function get_models(): Collection
    {
        $modelsPath = config('category.models_path');

        $models = collect(File::allFiles(base_path() . '/' . str_replace('\\', '/', lcfirst($modelsPath))))
            ->map(function ($item) use ($modelsPath) {
                $path = $item->getRelativePathName();

                return sprintf(
                    '%s%s',
                    $modelsPath,
                    strtr(substr($path, 0, strrpos($path, '.')), '/', '\\')
                );
            })
            ->filter(function ($class) {
                $valid = false;

                if (class_exists($class)) {
                    $reflection = new \ReflectionClass($class);
                    $valid = $reflection->isSubclassOf(Model::class)
                        && !$reflection->isAbstract();
                }

                return $valid;
            });

        return $models->values();
    }
}

if (!function_exists('is_model_using_either_category_trait')) {
    /**
     * Check if a class uses one of these traits: HasCategory | HasCategories
     *
     * @param string $modelClass
     *
     * @return bool
     */
    function is_model_using_either_category_trait(string $modelClass): bool
    {
        $modelTraits = class_uses($modelClass);

        return in_array(HasCategory::class, $modelTraits) || in_array(HasCategories::class, $modelTraits);
    }
}

if (!function_exists('is_model_using_category_trait')) {
    /**
     * Check if a class uses the HasCategory trait
     *
     * @param string $modelClass
     *
     * @return bool
     */
    function is_model_using_category_trait(string $modelClass): bool
    {
        $modelTraits = class_uses($modelClass);

        return in_array(HasCategory::class, $modelTraits);
    }
}

if (!function_exists('is_model_using_categories_trait')) {
    /**
     * Check if a class uses the HasCategories trait
     *
     * @param string $modelClass
     *
     * @return bool
     */
    function is_model_using_categories_trait(string $modelClass): bool
    {
        $modelTraits = class_uses($modelClass);

        return in_array(HasCategories::class, $modelTraits);
    }
}
